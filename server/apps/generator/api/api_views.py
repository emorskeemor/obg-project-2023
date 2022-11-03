from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import response, status
from rest_framework.exceptions import ValidationError

import io
import csv

from .serializers import (
    OptionBlocksSerializer,BlockSerializer,
    InsertTogetherSerializer,PregenerateSerializer
)
from apps.generator.models import (
    OptionBlocks,Block,InsertTogether,
)

from apps.environment.models import (
    GenerationSettings,Room
)

from apps.students.models import (
    Choice, Student, Option
)

from django.shortcuts import get_object_or_404  

from blocks.core.pregenerate.clean import populate_with_id, clean_options

from core.utils import parse_memory_handler

class GeneratorViewSet(ViewSet):
    
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=["post"])
    def run(self, request):
        # shortcut
        
        
        serialized = PregenerateSerializer(data=request.data)
        
        
        if serialized.is_valid(raise_exception=True):
            
            cleaned = serialized.data.get
            
            room = get_object_or_404(Room, code=cleaned("room_code"))
            settings = get_object_or_404(
                GenerationSettings, 
                room=room,
                title=cleaned("settings_title")
                )
            # we are either get the data from a csv or we are reading from a database
            # and converting it to a dictionary
            if cleaned("data_using_csv") is True:
                
                data = parse_memory_handler(request, "data_csv", slice(4))
                data = populate_with_id([clean_options(opts, 4) for opts in data])
            else:
                data = self.students_from_room(room)
                    
                    
            print(data)
                
        return response.Response({"data":"successs"}, status=status.HTTP_200_OK)
    
    @staticmethod
    def students_from_room(room):
        data = {}
        students = Student.objects.prefetch_related("options").filter(room=room)
        for student in students:
            options = []
            for option in student.options.all():
                options.append(option.subject_code)
            data[student.uuid] = options

      
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