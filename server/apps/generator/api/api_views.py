from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework import response, status, exceptions, permissions
from rest_framework.request import Request

import json

from typing import Dict
# serializers
from .serializers import (
OptionBlocksSerializer,BlockSerializer,
    InsertTogetherSerializer,GenerationSerializer
)
# models
from apps.generator.models import (
    OptionBlocks,Block,InsertTogether, BlockSubject
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
from bloc.core.post_generate.evaluation import EvaluationUtility, EmptyEvaluatedObject
from bloc.core.generate.utility import Generator, Node
from bloc.core.exceptions import OperationFailed
from bloc.core import protocols
from bloc.core.post_generate.operations import get_operation_report
from bloc.core.post_generate import validators, graphs, blocks

from drf_yasg.utils import swagger_auto_schema

from core.utils import csv_file_to_list

import operator

SUBJECT_CODE_ATTR = "title"
EBACC_FIELD_LOOKUP = "title"

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
        form_data = self._load_form_data(request)
        get = form_data.get
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
            options, override = self._get_room_subjects(room, use=SUBJECT_CODE_ATTR)
        # handle validators
        validate = [
            validators.MaxOptionsValidator(
                maximum=room_settings.max_subjects_per_block
            ),
            validators.StrictMultipleInsertionValidator(Node)
        ]
        if room_settings.blocks_must_align:
            validate.append(validators.PerfectAlignmentValidator())
        # handle protocols
        AVAILABLE_PROTOCOLS = {
            "protocol_A": protocols.ProtocolA,
            "protocol_B": protocols.ProtocolB,
            "protocol_C": protocols.ProtocolC,
            "protocol_D": protocols.ProtocolD,
            "protocol_E": protocols.ProtocolE,
        }
        protocol_id:str = get("protocol")
        protocol_id = protocol_id.replace(" ", "_")
        protocol = AVAILABLE_PROTOCOLS.get(protocol_id)
        if protocol is None:
            raise exceptions.ValidationError({"detail":"unknown protocol"})
        protocol = self._handle_protocol(protocol, form_data)
        if protocol == protocols.ProtocolC and get("order_options", False):
            print("ordering")
            options = sorted(options)
        # instansiate the generator
        generator = Generator(
            # provide default data
            data=data,
            options=options,
            blocks=room_settings.blocks,
            max_class_size=room_settings.class_size,
            ebacc=settings.EBACC_SUBJECTS,
            protocol=protocol,
            # other data
            debug=settings.GENERATOR_DEBUG,
            # provide the validators
            validators=validate

        )          
        generator.setup()  
        generator.classes.update(**override)
        
        # handle double inserts
        available_options = AvailableOption.objects.filter(option_choices__room=room)
        
        double_inserts = InsertTogether.objects.filter(settings=room_settings)
        for double_insert in double_inserts:
            # target = double_insert.target.subject_code
            target = getattr(available_options.get(option=double_insert.target), SUBJECT_CODE_ATTR)
   
            targets = [getattr(available_options.get(option=opt), SUBJECT_CODE_ATTR) for opt in double_insert.targets.all()]
            generator.insert_together(target,*targets)
        # EXECUTE THE GENERATION PROCESS
        generator.freeze()
        generator.execute()
        generator.evaluate()
        if isinstance(generator.evaluation, EmptyEvaluatedObject):
            generator_data = {
                "blocks": generator.evaluation.blocks,
                "students": {"success":[], "failed": []},
                "all": generator.data,
                "success": generator.evaluation.success_percentage,
                "debug": generator.debug_data,
                "rules_followed": False,
                "protocol_used": str(protocol)
            }
            generator.reset()

            return response.Response(generator_data, status=status.HTTP_200_OK)
        # handle the serialization. We need to handle the difference between using a
        # csv and a database as the csv will not have names
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
            serialized["success"][value]["uuid"] = str(value)
        for value in serialized.get("failed"):
            name = "Anonymous"
            email = "Not given"
            if not data_using_csv:
                student = students.get(uuid=value)
                name = f"{student.first_name} {student.last_name}"
                email = student.email
            serialized["failed"][value]["name"] = name
            serialized["failed"][value]["email"] = email
            serialized["failed"][value]["uuid"] =  str(value)
            
        blocks = generator.evaluation.blocks.with_counts(room_settings.class_size)
        generator.debug_data["generation_time"] = round(generator.debug_data["generation_time"], 4)
        generator_data = {
            "blocks": blocks.raw(),
            "students": serialized,
            "all": generator.data,
            "success": generator.evaluation.success_percentage,
            "debug": generator.debug_data,
            "rules_followed": True,
            "class_size": room_settings.class_size,
            "blocks_meta": blocks.remaining
        }
        # DEBUG PURPOSES ONLY
        generator.reset()
       
        return response.Response(generator_data, status=status.HTTP_200_OK)
    

    @action(methods=["post"], detail=False, url_path="pre-generate-statistics")
    def pre_generate_statitics(self, request):
        '''
        return pre-generate statistics e.g. popularity of each subjects and pathways
        '''
        # define some initial data
        get = self._load_form_data(request).get
        room = get_object_or_404(Room, code=get("room_id"))
        available_choices = get_object_or_404(AvalilableOptionChoices, room=room)
        options = {}
        ebacc_subjects = {
            "humanities":[],
            "languages":[],
            "sciences":[],
            "vocational":[],
            "not-applicable": [],
        }
        # get the option codes to be used
        for available_option in AvailableOption.objects.filter(option_choices=available_choices):
            
            code = getattr(available_option, SUBJECT_CODE_ATTR)
            options[code] = getattr(available_option, EBACC_FIELD_LOOKUP)
            ebacc_subjects[AvailableOption.EBACC(available_option.ebacc).label.lower()].append(code)
        ebacc_subjects.pop("not-applicable")
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
        pathway_pie_chart = graphs.PathwayPieChart(data=data, ebacc=ebacc_subjects)
        pathway_pie_chart.serialize()
        
        # define our context to send over
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
            room=get_object_or_404(Room, code=get("code")),
            use=SUBJECT_CODE_ATTR
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
        try:
            report = get_operation_report(
                operations=get("operations"),
                blocks=get("initial"),
                ignore_keys=["id", "students"],
                linear=get("linear", False),
                
                )
        except OperationFailed as error:
            raise exceptions.ValidationError({
                "detail": error.message
            })
        blocks.Blocks._data = get("all_students", {})
        blocks.Blocks._options = list(get("options", {}).keys())
        new_blocks = blocks.Blocks.load_exisiting(get("initial"))    
        new_blocks._counts = get("meta")
        counts = new_blocks.count_difference_using_initial()
        new_blocks._counts["remaining"] = counts
        new_blocks._counts["counts"] = new_blocks.total_counts()
        new_blocks._counts["failed"] = new_blocks.total_failed_counts()
        
        payload = {
            "report": report,
            "meta": new_blocks.remaining
        }
        

        return response.Response(payload, status=status.HTTP_200_OK)
    
    ##############################################
    # PRVIVATE METHODS
    ##############################################

    @staticmethod
    def _students_from_room(room: Room) -> Dict:
        '''gets the students from a given room in the database and return it as a dict'''
        data = {}
        students = Student.objects.prefetch_related("choices").filter(room=room).order_by("first_name")
        available = AvailableOption.objects.filter(option_choices__room=room)
        for student in students:
            if not student.ignore:
                options = []
                for choice in student.choices.all():
                    if not choice.reserve:
                        choice = available.get(option=choice.option)
                        options.append(getattr(choice, SUBJECT_CODE_ATTR))
                data[str(student.uuid)] = options
        return data
      
    @staticmethod
    def _get_room_subjects(room: Room, use="subject_code"):
        '''returns the subjects that link to a given room'''
        override = {}
        choices = get_object_or_404(
            AvalilableOptionChoices,
            room=room, 
            )
        options = []
        for available_option in AvailableOption.objects.filter(option_choices=choices):
            # uses subject code as reference
            code = getattr(available_option, use)
            options.append(code)
            if available_option.classes is not None:
                override[code] = available_option.classes
        return options, override
    
    @staticmethod
    def _load_form_data(request: Request) -> dict:
        payload = request.data.get("payload")
        if payload is None:
            raise exceptions.ValidationError({"detail":"payload required as form data"})
        return json.loads(payload)
    
    @staticmethod
    def _handle_protocol(protocol: protocols.BaseProtocol, form_data:dict):
        if protocol == protocols.ProtocolB:
            reverse = form_data.get("reverse_options", False)
            return protocol(reversed=reverse)
        elif protocol == protocols.ProtocolD:
            target_percentage = form_data.get("target_percentage")
            if target_percentage is None:
                raise exceptions.ValidationError(
                    {"detail":"target_percentage is required"}
                )
            return protocol(target_percentage=int(target_percentage))
        elif protocol == protocols.ProtocolE:
            iterations = form_data.get("iterations")
            if iterations is None:
                raise exceptions.ValidationError(
                    {"detail":"iterations is required"}
                )
            return protocol(iters=int(iterations))
        else:
            return protocol()
    
import uuid
    
class OptionBlockViewset(ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OptionBlocksSerializer
    queryset = OptionBlocks.objects.all()
    
    def create(self, request: Request, *args, **kwargs):
        
        blocks = request.data.get("blocks")
        if blocks is None:
            raise exceptions.ValidationError({"detail":"blocks required"})
        room_code = request.data.get("code")
        room = get_object_or_404(Room, code=room_code)
        title = request.data.get("title", str(uuid.uuid4()))
        if OptionBlocks.objects.filter(room=room, title=title).exists():
            raise exceptions.ValidationError(
                {"detail":"you already haved saved option blocks named '%s'" % title}
                )
        option_blocks = OptionBlocks.objects.create(
            room=room,
            title=title,
            number_of_blocks=len(blocks),
            success_percentage=request.data.get("success"),
            generation_time=request.data.get("generation_time"),
            completed_nodes=request.data.get("completed_nodes"),
            generated_nodes=request.data.get("generated_nodes"),
            created_by=request.user
        )
        # subjects = get_object_or_404(AvalilableOptionChoices, room=room).options.all()
        subjects = AvailableOption.objects.filter(option_choices__room=room)
        
        for index, block in enumerate(blocks):
            new_block = Block(
                blocks=option_blocks,
                block_id=index,
                number_of_subjects=len(block)
            )
            new_block.save()
            for subject in block:
                obj = subjects.filter(**{SUBJECT_CODE_ATTR:subject[0]})
                if not obj.exists():
                    raise exceptions.ValidationError({"detail": "subject '%s' was not found as an available subject" % subject})
                obj = obj[0].option
                # new_block.options.add(obj)
                BlockSubject.objects.create(
                    option=obj,
                    block=new_block,
                    students=subject[1]
                )
    
        return response.Response({"detail":"blocks created"}, status=status.HTTP_200_OK)
    
class BlockViewset(ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    
class InsertTogetherViewset(ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InsertTogetherSerializer
    queryset = InsertTogether.objects.all()
    
    @action(methods=["get"], detail=True, url_path="room-rules")
    def room_rules(self, request, pk, *args, **kwargs):
        '''
        returns data about the insert rules
        '''
        room = get_object_or_404(Room, code=pk)
        self.check_object_permissions(request, room)
        settings = get_object_or_404(GenerationSettings, room=room)
        inserts = InsertTogether.objects.filter(settings=settings)
        serialized = self.serializer_class(inserts, many=True)
        options = []
        # also attach the available options so it can be used to create
        # a new room later
        for available_option in AvailableOption.objects.filter(option_choices__room=room):
            options.append({
                "label": available_option.title,
                "value": available_option.pk
            })
            
        payload = {
            "inserts": serialized.data,
            "available_options": options
        }
        return response.Response(payload, status=status.HTTP_200_OK)
    
    def create(self, request: Request, *args, **kwargs):
        get = request.data.get
        room = get_object_or_404(Room, code=get("room_code"))
        # self.check_object_permissions(request, room)
        settings = get_object_or_404(GenerationSettings, room=room)
        target = get_object_or_404(AvailableOption, pk=get("target_pk"))
        new_insert = InsertTogether(settings=settings, target=target.option)
        new_insert.save()
        targets = []
        for subject in get("targets", []):
            targets.append(
                get_object_or_404(AvailableOption, pk=subject.get("value")).option
            )
        new_insert.targets.add(*targets)
        
        return response.Response()
    
 