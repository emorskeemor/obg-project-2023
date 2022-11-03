from rest_framework.serializers import ModelSerializer

from apps.students.models import Student, Choice, Option, Requirement


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

