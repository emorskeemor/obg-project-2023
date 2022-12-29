from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.request import Request

from django.shortcuts import get_object_or_404
from copy import deepcopy

from apps.students.models import Student, Choice, Option, Requirement
from apps.generator.models import InsertTogether

from apps.environment.api import (
    serializers as env_serializers,
    permissions as env_permissions,
)
from apps.environment.models import Room, AvalilableOptionChoices, GenerationSettings, AvailableOption

from core.utils import csv_file_to_list, valid_uuid_or_error, load_form_data, get_data_from_csv

from .serializers import (
    ChoiceSerializer, 
    OptionSerializer, 
    StudentSerializer,
    StudentDumpSerializer
    )
from .pagination import StudentPaginator

from drf_yasg.utils import swagger_auto_schema

from bloc.core.pre_generate.validate import clean_options

import names

# implmeneted the serializer here to avoid circular imports
class RequirementSerializer(ModelSerializer):
    '''
    serialize requirement 
    '''
    room = env_serializers.RoomSerializer(read_only=True)
    option = OptionSerializer(read_only=True)
    
    class Meta:
        model = Requirement
        fields = "__all__"

class StudentViewset(ModelViewSet):
    '''
    views to access students
    '''
    permission_classes = [AllowAny, env_permissions.RoomAccessPermission]
    serializer_class = StudentSerializer
    queryset = Student.objects.all().order_by("first_name")
    pagination_class = StudentPaginator
    
    @swagger_auto_schema(request_body=StudentDumpSerializer)
    @action(detail=False, methods=["post"], url_path="dump-students")
    def dump_students(self, request: Request):
        '''
        Dump csv containing student options into the database.
        WARNING : Caution while using this endpoint as it will create many records in the DB
        '''
        # load the form data and parse the csv file given
        data = load_form_data(request)
        serialized = StudentDumpSerializer(data=data)
        serialized.is_valid(raise_exception=True)
        get = serialized.data.get
        data = get_data_from_csv(request)
        
        room_code = get("room_code")
        room = get_object_or_404(Room, code=room_code)
        self.check_object_permissions(request, room)
        options_using = get("options_using")
        
        choices = get_object_or_404(
            AvalilableOptionChoices,
            title=options_using,
            room=room
            )
        available_options = choices.options.all()
        for options in data:
            options = clean_options(options, max_opts=get("max_opts_per_student"))
            first_name = "anonymous"
            last_name = "user"
            if get("generate_dummy_names"):
                first_name = names.get_first_name()
                last_name = names.get_last_name()
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                room=room,
                max_reserves=get("allowed_reserves"),
                max_choices=get("max_opts_per_student"),
                email="%s.%s@%s.co.uk" % (first_name, last_name, room.domain)
            )
            student.save()
            
            student_choices = []
            for option_code in options:
                # warning: ambiguous 404
                option = get_object_or_404(available_options, subject_code=option_code)
                new_choice = Choice(
                    option=option,
                    student =student
                )
                student_choices.append(new_choice)
            Choice.objects.bulk_create(student_choices)
            
        return Response({"message":"successful"}, status=status.HTTP_200_OK)
        
    def retrieve(self, request, pk):
        '''
        return a student with their ordered options and their reserve options
        '''
        student = get_object_or_404(Student.objects.prefetch_related("options"), uuid=pk)
        # order the students' choices by priority and get the reserve options
        choices = Choice.objects.filter(student=student).order_by("priority")
        reserved = choices.filter(reserve=True)
        ordered_options = []
        # serialize main options and add it to the serialized student data
        for choice in choices.filter(reserve=False):
            ordered_options.append(OptionSerializer(choice.option).data)
        serialized = StudentSerializer(student)
        serialized_data = deepcopy(serialized.data)
        serialized_data["options"] = ordered_options
        # serialize the reserve options and add it to the serialized student data
        serialized_reserves = []
        for reserve in reserved:
            serialized_reserves.append(OptionSerializer(reserve.option).data)
        serialized_data["reserves"] = serialized_reserves
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    @action(methods=["get", "put"], url_path="room-students", detail=True)
    def room_students(self, request:Request, pk):
        '''
        returns all students attached to a room
        '''
        if request.method == "GET":
            room = get_object_or_404(Room, code=pk)
            data = []
            for student in room.students.all():
                # separate the reserves from the actual options
                reserves, main = [], []
                for choice in student.choices.all():
                    opt_serialized = OptionSerializer(choice.option).data
                    if choice.reserve:
                        reserves.append(opt_serialized)
                    else:
                        main.append(opt_serialized)
                serialized = self.serializer_class(student)
                to_add = serialized.data.copy()
                to_add["reserves"] = reserves
                to_add["options"] = main
                data.append(to_add)                
                
            return Response(data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            room = get_object_or_404(Room, code=pk)
            students = room.students.all()
            
            for student_data in request.data.get("students", []):
                student: Student = students.get(uuid=student_data.get("uuid"))
                serialized = self.serializer_class(instance=student, data=student_data)
                serialized.is_valid(raise_exception=True)
                serialized.save()
            
            return Response({}, status=status.HTTP_200_OK)

    
class ChoiceViewset(ModelViewSet):
    '''
    views to access choices
    '''
    permission_classes = [AllowAny]
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
    
    @action(detail=False, methods=["get"], url_path="student_choices")
    def students_options(self, request):
        '''
        gets a student's subjects if any
        '''
        get = request.GET.get
        student = get_object_or_404(Student, uuid=get("student"))
        
        serialized = OptionSerializer(
            student.options.all().order_by("title").values(
                "uuid", "subject_code", "description", "title"
                ), 
            many=True
            )
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["put"], url_path="update_student_options")
    def update_student_options(self, request, pk=None):
        '''
        update the students options by providing the new options and new reserve options.
        All previous options will be overriden.
        '''
        student = get_object_or_404(Student, pk=pk)
        options = student.options.all()
        
        # first serialize the incoming data to ensure if conforms to our formatting standards
        main_options = request.data.get("main_options")
        serialized_main_options = OptionSerializer(data=main_options, many=True)
        serialized_main_options.is_valid(raise_exception=True)
        
        # handle the reserve options
        reserve_options = request.data.get("reserve_options")
        serialized_reserves = OptionSerializer(data=reserve_options, many=True)
        serialized_reserves.is_valid(raise_exception=True)
        # mark these options as reserve
        for reserve in reserve_options:
            reserve["reserve"] = True
            main_options.append(reserve)          
        
        # get the room so we can get the rules that the options must abide by   
        code = request.data.get("code")
        domain = request.data.get("domain")
        
        room = get_object_or_404(Room, code=code, domain=domain)
        settings = get_object_or_404(GenerationSettings, room=room)
        rules = InsertTogether.objects.filter(settings=settings)
        
        forbidden = []
        for rule in rules:
            forbidden.append([rule.target] + list(rule.targets.all()))
        
        options = Option.objects.all()
        # create the new choices
        new_option_choice = []
        # create our new set of options
        for index, option in enumerate(main_options):
            option_uuid = option.get("uuid")
            reserve = option.get("reserve", False)
            valid_uuid_or_error(option_uuid)
            option = get_object_or_404(options, uuid=option_uuid)
            new_choice = Choice(
                student=student,
                option=option,
                priority=index,
                reserve=reserve
            )
            new_option_choice.append(new_choice)
        # see if the students options contain subjects that are not allowed to be together.
        # choices that are marked as reserve will not influence the rule
        for rule in forbidden:
            count = 0
            for choice in new_option_choice:
                if choice.option in rule and choice.reserve is False:
                    count += 1
            if count == len(rule):  
                raise exceptions.ValidationError(
                    {"detail":f"Options ({', '.join([option.title for option in rule])}) cannot be chosen together"}
                    )
                
        # clear all choices
        for option in options:
            student.options.remove(option)
            
        # save the new set of options        
        Choice.objects.bulk_create(new_option_choice)
        
        return Response({"detail":"success"}, status=status.HTTP_200_OK)

class OptionViewset(ModelViewSet):
    '''
    views to access options
    '''
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    
    @action(methods=["post"], detail=False, url_path="dump-options")
    def dump_options(self, request):
        '''
        dump csv containing options and option codes to the database.
        WARNING : Caution while using this endpoint as it will create many records in the DB

        '''
        options = csv_file_to_list(request, "options", slice(2))
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
    '''
    views to access requirements that are linked to options
    '''
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()
