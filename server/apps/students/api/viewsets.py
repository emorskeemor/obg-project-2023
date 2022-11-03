from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from apps.students.models import Student, Choice, Option, Requirement
from apps.environment.api.serializers import RoomSerializer
from core.utils import is_valid_uuid

from .serializers import (
    ChoiceSerializer, 
    OptionSerializer, 
    StudentSerializer,
    )

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

    # def retrieve(self, request, uuid):
    #     if not is_valid_uuid(uuid):
    #         raise exceptions.ValidationError("uuid invalid")
    #     obj = get_object_or_404(Student, uuid=uuid)
    #     serializer = StudentSerializer(obj)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


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
    
class RequirementViewSet(ModelViewSet):
    '''views to access requirements that are linked to options'''
    permission_classes = [AllowAny]

    serializer_class = RequirementSerializer
    queryset = Requirement.objects.all()
