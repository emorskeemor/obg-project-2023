from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import response, status, exceptions

import io
import csv
import uuid

from functools import partial

from typing import Dict
# serializers
from .serializers import (
    OptionBlocksSerializer,BlockSerializer,
    InsertTogetherSerializer,PregenerateSerializer
)
# models
from apps.generator.models import (OptionBlocks,Block,InsertTogether)
from apps.environment.models import (GenerationSettings,Room, AvalilableOptionChoices, AvailableOption)
from apps.students.models import (Choice, Student, Option)
# django
from django.shortcuts import get_object_or_404  
# option block api
from blocks.core.pregenerate.clean import populate_with_id, clean_options
from blocks.core.generate.utility import Generator
from blocks.core.postgenerate.evaluation import EvaluationUtility

from core.utils import csv_file_to_list

class GerneratorViewset(ViewSet):
    '''
    core viewset for running the option block generator
    '''
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=["post"])
    def run(self, request):
        '''
        runs the option block generation process
        '''
        serialized = PregenerateSerializer(data=request.data)
        file_to_list = partial(csv_file_to_list, request)
        
        if serialized.is_valid(raise_exception=True):
            cleaned_get = serialized.data.get
            room = get_object_or_404(Room, code=cleaned_get("room_code"))
            settings = get_object_or_404(
                GenerationSettings, 
                room=room,
                title=cleaned_get("settings_title")
                )
            # we are either get the data from a csv or we are reading from a database
            # and converting it to a dictionary
            if cleaned_get("data_using_csv") is True:
                options = file_to_list(
                    name="data_csv", 
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
                    name="options_csv", 
                    slice_func=1,
                    hints="each line requires two items 'subject_name','subject_code'"
                )
            else:
                choices = get_object_or_404(
                    AvalilableOptionChoices,
                    room=room, 
                    title=cleaned_get("options_title")
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
                num_blocks=settings.blocks,
                class_size=settings.class_size
            )          
            generator.prepare_generation()     
            # handle double inserts
            double_inserts = InsertTogether.objects.filter(settings=settings)
            for double_insert in double_inserts:
                target = double_insert.target.subject_code
                targets = [
                    opt["subject_code"] for opt in double_insert.targets.values("subject_code")
                    ]
                generator.insert_together(target,*targets)
            generator.debug()
            generator.update_classes_per_subject(**override)
            generator.run_generation()
            generator.evaluate_generation(
                ebacc={
                    "humanities":["Hi","Ge"],
                    "languages":["Fr","Sn"],
                    "sciences":["Sc","Co"],
                    "vocational":["Co","Bs","Eg","Cb"]
                }
            )

            
            payload = {
                "blocks": generator.best_evaluation.blocks,
                "success": generator.best_evaluation.success_percentage
            }
            
            return response.Response(payload, status=status.HTTP_200_OK)
    
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

      
class OptionBlockViewset(ModelViewSet):
    
    permission_classes = [AllowAny]
    serializer_class = OptionBlocksSerializer
    queryset = OptionBlocks.objects.all()
    
class BlockViewset(ModelViewSet):
    
    permission_classes = [AllowAny]
    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    
class InsertTogetherViewset(ModelViewSet):
    
    permission_classes = [AllowAny]
    serializer_class = InsertTogetherSerializer
    queryset = InsertTogether.objects.all()