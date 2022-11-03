from rest_framework.serializers import ModelSerializer

from apps.students.models import Student, Choice, Option, Requirement
from apps.environment.api.serializers import RoomSerializer


class ChoiceSerializer(ModelSerializer):

    class Meta:
        model = Choice
        fields = "__all__"

class OptionSerializer(ModelSerializer):

    class Meta:
        model = Option
        fields = "__all__"

class StudentSerializer(ModelSerializer):

    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = "__all__"

class RequirementSerializer(ModelSerializer):
    
    room = RoomSerializer(read_only=True)
    option = OptionSerializer(read_only=True)
    
    class Meta:
        model = Requirement
        fields = "__all__"