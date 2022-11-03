from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from apps.students.models import Student, Choice, Option, Requirement
from apps.environment.api.serializers import RoomSerializer
from apps.environment.models import Room, AvalilableOptions

from core.utils import parse_memory_handler

from .serializers import (
    ChoiceSerializer, 
    OptionSerializer, 
    StudentSerializer,
    StudentDumpSerializer
    )


from blocks.core.pregenerate.clean import clean_options

import names
# implmeneted the serializer here to avoid circular imports
class RequirementSerializer(ModelSerializer):
    '''serialize requirement objects'''
    room = RoomSerializer(read_only=True)
    option = OptionSerializer(read_only=True)
    
    class Meta:
        model = Requirement
        fields = "__all__"

class StudentViewset(ModelViewSet):
    '''views to access students'''
    permission_classes = [AllowAny]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    lookup_field = "uuid"

    @action(detail=False, methods=["post"])
    def dump(self, request):
        
        data = parse_memory_handler(request, "data", slice(4))
        
        serialized = StudentDumpSerializer(data=request.data)
        if serialized.is_valid():
            get = serialized.data.get
            room_code = get("room_code")
            room = get_object_or_404(Room, code=room_code)
            
            options_using = get("options_using")
            
            choices = get_object_or_404(
                AvalilableOptions,
                title=options_using,
                room=room
                )
            available_options = choices.options.all()
            for options in clean_options(data, get("max_opts_per_student")):
                first_name = None,
                last_name = None
                if get("generate_dummy_names"):
                    first_name = names.get_first_name()
                    last_name = names.get_last_name()
                student = Student.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    room=room,
                    email="%s.%s@%s.co.uk" % (first_name, last_name, room.domain)
                )
                student.save()
                
                student_choices = []
                for option_code in options:
                    option = available_options.get(subject_code=option_code)
                    new_choice = Choice(
                        option=option,
                        student =student
                    )
                    student_choices.append(new_choice)
                Choice.objects.bulk_create(student_choices)
                
                
            return Response({"message":"successful"}, status=status.HTTP_200_OK)


class ChoiceViewset(ModelViewSet):
    '''views to access choices'''
    permission_classes = [AllowAny]

    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

class OptionViewset(ModelViewSet):
    '''views to access options'''
    permission_classes = [AllowAny]

    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    
    @action(methods=["post"], detail=False)
    def dump(self, request):
        options = parse_memory_handler(request, "options", slice(2))
        raise Exception("saftey")
        new_options = []
        for name, code in options:
            new_options.append(
                Option(
                    title=name,
                    subject_code=code
                )
            )
        Option.objects.bulk_create(new_options)
            
        return Response({"message":"successful"}, status=status.HTTP_200_OK)
    
class RequirementViewSet(ModelViewSet):
    '''views to access requirements that are linked to options'''
    permission_classes = [AllowAny]

    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()
