from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework import response, status, exceptions, permissions

from functools import partial
import json

from typing import Dict
# serializers
from .serializers import (
OptionBlocksSerializer,BlockSerializer,
    InsertTogetherSerializer,GenerationSerializer
)
# models
from apps.generator.models import (
    OptionBlocks,Block,InsertTogether
    )
from apps.environment.models import (
    GenerationSettings,Room, AvalilableOptionChoices, AvailableOption
    )
from apps.students.models import Student, Choice
# permissions
from apps.environment.api.permissions import RoomAccessPermission

# django
from django.shortcuts import get_object_or_404  
from django.conf import settings

# generator
from bloc.core.pre_generate.validate import populate_with_id, clean_options
from bloc.core.pre_generate.statistics import subject_counts, group_by_class, filter_grouped_by
from bloc.core.post_generate.pathway import DEFAULT_PATHWAYS
from bloc.core.post_generate.evaluation import EvaluationUtility
from bloc.core.generate.utility import Generator
from bloc.core.exceptions import PathwayFailed
from bloc.core import protocols
from bloc.core.post_generate.operations import get_operation_report
from bloc.core.post_generate import graphs

from drf_yasg.utils import swagger_auto_schema

from core.utils import csv_file_to_list

import operator

def get_data_from_csv(request):
    return csv_file_to_list(
        request,
        name=settings.DATA_CSV_LOOKUP, 
        slice_func=slice(4),
        hints="each line requires n items of 'subject_codes'"
    )
    
def get_options_from_csv(request):
    return csv_file_to_list(
        request,
        name=settings.OPTIONS_CSV_LOOKUP, 
        slice_func=1,
        hints="each line requires two items 'subject_name','subject_code'"
    )

class GerneratorViewset(ViewSet):
    '''
    core viewset for running the option block generator
    '''
    permission_classes = [permissions.IsAuthenticated, RoomAccessPermission]
    
    #############################################
    # CORE VIEWS
    #############################################
    
    @swagger_auto_schema(request_body=GenerationSerializer)
    @action(detail=False, methods=["post"])
    def run(self, request):
        '''
        Runs the option block generation process
        '''
        get = self._load_form_data(request).get
        room = get_object_or_404(
            Room, 
            code=get("code"),
            )
        room_settings = get_object_or_404(
            GenerationSettings, 
            room=room,
            )
        self.check_object_permissions(request, room)
        # we are either get the data from a csv or we are reading from a database
        # and converting it to a dictionary
        data_using_csv = get("data_using_csv")
        if data_using_csv is True:
            options = get_data_from_csv(request)
            data = populate_with_id([clean_options(opts, 4) for opts in options])
        else:
            data = self._students_from_room(room)
        # get the subject codes either from a CSV or from a database
        override = {}
        if get("subjects_using_csv"):
            options = get_options_from_csv(request)
        else:
            options, override = self._get_room_subjects(room)
        # give the generator the initial variables and prepare it
        generator = Generator(
            data=data,
            options=options,
            blocks=room_settings.blocks,
            max_class_size=room_settings.class_size,
            ebacc=settings.EBACC_SUBJECTS,
            protocol=protocols.ProtocolB(),
            debug=settings.GENERATOR_DEBUG
        )          
        generator.setup()  
        generator.classes.update(**override)
        
        # handle double inserts
        double_inserts = InsertTogether.objects.filter(settings=room_settings)
        for double_insert in double_inserts:
            target = double_insert.target.subject_code
            targets = [
                opt["subject_code"] for opt in double_insert.targets.values("subject_code")
                ]
            generator.insert_together(target,*targets)
        # EXECUTE THE GENERATION PROCESS
        generator.freeze()
        generator.execute()
        generator.evaluate()
        
        students = Student.objects.filter(room=room)
        serialized = generator.evaluation.serialize(include_paths=True)
        for value in serialized.get("success"):
            name = "Anonymous"
            email = "Not given"
            if not data_using_csv:
                student = students.get(uuid=value)
                name = f"{student.first_name} {student.last_name}"
                email = student.email
            serialized["success"][value]["name"] = name
            serialized["success"][value]["email"] = email
        for value in serialized.get("failed"):
            name = "Anonymous"
            email = "Not given"
            if not data_using_csv:
                student = students.get(uuid=value)
                name = f"{student.first_name} {student.last_name}"
                email = student.email
            serialized["failed"][value]["name"] = name
            serialized["failed"][value]["email"] = email
            
        generator_data = {
            "blocks": generator.evaluation.blocks,
            "students": serialized,
            "all": generator.data,
            "success": generator.evaluation.success_percentage,
            "debug": generator.debug_data
        }
        # DEBUG PURPOSES ONLY
        generator.evaluation.pprint()
       
        return response.Response(generator_data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_path="pre-generate-statistics")
    def pre_generate_statitics(self, request):
        '''
        return pre-generate statistics e.g. popularity of each subjects and pathways
        '''
        # get some initial data
        get = self._load_form_data(request).get
        room = get_object_or_404(Room, code=get("room_id"))
        options = {}
        for available_option in AvailableOption.objects.all():
            code = available_option.option.subject_code
            options[code] = available_option.option.title
            
        # get the data either using a csv or database
        if get("using_database") is False:
            data_opts = get_data_from_csv(request)
            data = populate_with_id([clean_options(opts, 4) for opts in data_opts])
        else:
            data = self._students_from_room(room)
        # get some variables to be commonly used by each graph
        classes = int(get("classes"))
        counts = subject_counts(data=data, option_codes=list(sorted(tuple(options.keys()))))
        
        # CLASH HEAT MAP GRAPH
        grouped = group_by_class(counts, class_size=24, maximum=4)
        clash_heat_map = graphs.ClashMatrixGraph(
            option_codes=filter_grouped_by(grouped, value=classes, operation=operator.eq).keys(),
            data=data
        )
        clash_heat_map.ignore(*get("ignore_subjects", []))
        clash_heat_map.level = int(get("max_clashes"))
        clash_heat_map.serialize()
        # SUBJECT POPULARITY BAR CHART
        popularity_bar_chart = graphs.SubjectPopularityBarChart(
            data=data,
            option_codes=options
        )
        popularity_bar_chart.serialize()
        # PATHWAY PIE CHART
        pathway_pie_chart = graphs.PathwayPieChart(data=data, ebacc=settings.EBACC_SUBJECTS)
        pathway_pie_chart.serialize()
        context = {
            # heat map
            "clash_heat_map": clash_heat_map.as_dict(),
            "popularity_bar_chart": popularity_bar_chart.as_dict(),
            "pathway_pie_chart": pathway_pie_chart.as_dict(),          
            # extra statistics
            "subject_codes": list(counts.keys()),
            "options": options,
            "number_of_students": len(data), 
            "number_of_subjects": sum([len(options) for options in data.values()]),
        }
        return response.Response(context, status=status.HTTP_200_OK)
    
    @action(methods=["post"], detail=False, url_path="validate-data-file")
    def validate_data_file(self, request):
        '''
        validates data file to be used in generation
        '''
        get = self._load_form_data(request).get
        opts, _ = self._get_room_subjects(
            room=get_object_or_404(Room, code=get("code"))
            )
        for student_opts in get_data_from_csv(request):
            for subject in student_opts:
                if subject not in opts and subject:
                    raise exceptions.ValidationError(
                        {"detail":f"subject '{subject}' does not exist in the available options for this room"}
                    )
        return response.Response(status=status.HTTP_200_OK)
    
    @action(methods=["post"], detail=False)
    def evaluate(self, request):
        '''
        evaluate a manipulated set of option blocks by using operations
        '''
        get = request.data.get
        EvaluationUtility._data = get("all_students")
        EvaluationUtility.EBACC = settings.EBACC_SUBJECTS
        report = get_operation_report(
            operations=get("operations"),
            blocks=get("initial"),
            ignore_keys=["id"]
            
            )
        print(report)
        return response.Response()
    
    ##############################################
    # PRVIVATE METHODS
    ##############################################

    @staticmethod
    def _students_from_room(room) -> Dict:
        '''gets the students from a given room in the database and return it as a dict'''
        data = {}
        students = Student.objects.prefetch_related("options").filter(room=room)
        for student in students:
            options = []
            for choice in Choice.objects.filter(student=student):
                if not choice.reserve:
                    options.append(choice.option.subject_code)
            data[str(student.uuid)] = options
        return data
      
    def _get_room_subjects(self, room):
        override = {}
        choices = get_object_or_404(
            AvalilableOptionChoices,
            room=room, 
            )
        options = []
        for available_option in AvailableOption.objects.filter(option_choices=choices):
            code = available_option.option.subject_code
            options.append(code)
            if available_option.classes is not None:
                override[code] = available_option.classes
        return options, override
    
    @staticmethod
    def _load_form_data(request) -> dict:
        payload = request.data.get("payload")
        if payload is None:
            raise exceptions.ValidationError({"detail":"payload required as form data"})
        return json.loads(payload)
    
    
    
class OptionBlockViewset(ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OptionBlocksSerializer
    queryset = OptionBlocks.objects.all()
    
class BlockViewset(ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    
class InsertTogetherViewset(ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InsertTogetherSerializer
    queryset = InsertTogether.objects.all()