from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from apps.students.models import Student, Choice, Option, Requirement
from core.utils import is_valid_uuid

from .serializers import (
    ChoiceSerializer, 
    OptionSerializer, 
    StudentSerializer,
    RequirementSerializer
    )

class StudentViewset(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    lookup_field = "uuid"

    def retrieve(self, request, uuid):
        if not is_valid_uuid(uuid):
            raise exceptions.ValidationError("uuid invalid")
        obj = get_object_or_404(Student, uuid=uuid)
        serializer = StudentSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class ChoiceViewset(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

class OptionViewset(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    
class RequirementViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()
