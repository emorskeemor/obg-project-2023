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
    GenerationSettings,Room, AvalilableOptionChoices
    )
from apps.environment.api.permissions import RoomAccessPermission
from apps.students.models import Student
# django
from django.shortcuts import get_object_or_404  
from django.conf import settings
# option block api
from blocks.core.pregenerate.clean import populate_with_id, clean_options
from blocks.core.pregenerate.statistics import subject_counts
from blocks.core.postgenerate.pathway import DEFAULT_PATHWAYS
from blocks.core.generate.utility import Generator
from blocks.core.exceptions import PathwayFailed

from drf_yasg.utils import swagger_auto_schema

from core.utils import csv_file_to_list

# views in the generator module should only be accessed by authorised users.

class GerneratorViewset(ViewSet):
    '''
    core viewset for running the option block generator
    '''
    permission_classes = [permissions.IsAuthenticated, RoomAccessPermission]
    
    @swagger_auto_schema(request_body=GenerationSerializer)
    @action(detail=False, methods=["post"])
    def run(self, request):
        '''
        Runs the option block generation process
        '''
        # serialized = GenerationSerializer(data=request.data)
        file_to_list = partial(csv_file_to_list, request)
        
        # serialized.is_valid(raise_exception=True)
        cleaned_get = json.loads(request.data.get("payload")).get
        room = get_object_or_404(
            Room, 
            code=cleaned_get("code"),
            # domain=cleaned_get("domain"),
            )
        room_settings = get_object_or_404(
            GenerationSettings, 
            room=room,
            # title=cleaned_get("settings_title")
            )
        self.check_object_permissions(request, room)
        # we are either get the data from a csv or we are reading from a database
        # and converting it to a dictionary
        if cleaned_get("data_using_csv") is True:
            options = file_to_list(
                name=settings.DATA_CSV_LOOKUP, 
                slice_func=slice(4),
                hints="each line requires n items of 'subject_codes'"
            )
            data = populate_with_id([clean_options(opts, 4) for opts in options])
        else:
            data = self.students_from_room(room)
        if data == {}:
            raise exceptions.ValidationError({
                "error":"cannot generate option block with no students"
            })
        # get the subject codes 
        override = {}
        if cleaned_get("subjects_using_csv"):
            options = file_to_list(
                name=settings.OPTIONS_CSV_LOOKUP, 
                slice_func=1,
                hints="each line requires two items 'subject_name','subject_code'"
            )
        else:
            choices = get_object_or_404(
                AvalilableOptionChoices,
                room=room, 
                # title=cleaned_get("options_title")
                )
            options = []
            for available_option in choices.options.through.objects.all():
                code = available_option.option.subject_code
                options.append(code)
                if available_option.classes is not None:
                    override[code] = available_option.classes
                    
        if options == []:
            raise exceptions.ValidationError({
                "error":"cannot generate option blocks with no option codes"
            })
        # give the generator the initial variables and prepare it
        generator = Generator(
            data=data,
            options_codes=options,
            num_blocks=room_settings.blocks,
            class_size=room_settings.class_size
        )          
        generator.prepare_generation()     
        generator.update_classes_per_subject(**override)
        # handle double inserts
        double_inserts = InsertTogether.objects.filter(settings=room_settings)
        for double_insert in double_inserts:
            target = double_insert.target.subject_code
            targets = [
                opt["subject_code"] for opt in double_insert.targets.values("subject_code")
                ]
            generator.insert_together(target,*targets)
        # debug which is defined in project settings module
        if settings.GENERATOR_DEBUG:
            generator.debug()
        if settings.NODE_DEBUG:
            generator.node.debug = True
        
        generator.run_generation()
        generator.evaluate_generation(
            ebacc={
                "humanities":["Hi","Ge"],
                "languages":["Fr","Sn"],
                "sciences":["Sc","Co"],
                "vocational":["Co","Bs","Eg","Cb"]
            }
        )
        
        gen_info = {
            "blocks": generator.best_evaluation.blocks,
            "success": generator.best_evaluation.success_percentage
        }
        
        return response.Response(gen_info, status=status.HTTP_200_OK)

    @staticmethod
    def students_from_room(room) -> Dict:
        '''gets the students from a given room in the database and return it as a dict'''
        data = {}
        students = Student.objects.prefetch_related("options").filter(room=room)
        for student in students:
            options = []
            for option in student.options.all():
                options.append(option.subject_code)
            data[student.uuid] = options
        return data
    
    @action(methods=["post"], detail=False, url_path="pre-generate-statistics")
    def pre_generate_statitics(self, request):
        # print(request.data)
        payload: dict = json.loads(request.data.get("payload"))
        file_to_list = partial(csv_file_to_list, request)

        room = get_object_or_404(Room, code=payload.get("room_id"))
        choices = get_object_or_404(
                AvalilableOptionChoices,
                room=room, 
                # title=cleaned_get("options_title")
                )
        options = {}
        for available_option in choices.options.through.objects.all():
            code = available_option.option.subject_code
            # options.append(code)
            options[code] = available_option.option.title
            # if available_option.classes is not None:
            #     override[code] = available_option.classes 
        if payload.get("using_database") is False:
            data_opts = file_to_list(
                name=settings.DATA_CSV_LOOKUP, 
                slice_func=slice(4),
                hints="each line requires n items of 'subject_codes'"
            )
            data = populate_with_id([clean_options(opts, 4) for opts in data_opts])
        else:
            data = self.students_from_room(room)
        popularity = subject_counts(data=data, option_codes=options.keys())
        actual = {options.get(code):count for code, count in popularity.items()}
        student_pathways = self.get_student_pathways(data)
        payload = {
            "subjects": list(actual.keys()),
            "counts": list(actual.values()),
            "pathways": list(student_pathways.keys()),
            "pathway_counts": list(student_pathways.values())
        }
        return response.Response(payload)
    
    @staticmethod
    def get_student_pathways(data):
        '''
        returns the pathway a set of options follow
        '''
        pathways = DEFAULT_PATHWAYS.copy()
        counts = dict.fromkeys(tuple(map(lambda x:x.__name__, pathways)), 0)
        ebacc = settings.EBACC_SUBJECTS
        for student, options in data.items():
            path = None
            for possible_path in pathways:
                try:
                    path = possible_path(ebacc)
                    path(*options)
                    break
                except PathwayFailed:
                    pass
            current = counts[path.__class__.__name__]
            counts[path.__class__.__name__] = current + 1
                
        return counts
        # raise an error meaning that the path ways we provided resulted in no
        # fallback pathway to be found

      
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