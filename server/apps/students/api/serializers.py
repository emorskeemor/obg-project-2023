from rest_framework.serializers import ModelSerializer

from apps.students.models import Student, Choice, Option, Requirement


class ChoiceSerializer(ModelSerializer):
    '''serialize choice objects'''
    class Meta:
        model = Choice
        fields = "__all__"

class OptionSerializer(ModelSerializer):
    '''serialize option objects'''
    class Meta:
        model = Option
        fields = "__all__"

class StudentSerializer(ModelSerializer):
    '''serialize student objects'''
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = "__all__"

