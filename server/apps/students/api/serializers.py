from rest_framework import serializers

from apps.students.models import Student, Choice, Option, Requirement


class ChoiceSerializer(serializers.ModelSerializer):
    '''serialize choice objects'''
    class Meta:
        model = Choice
        fields = "__all__"

class OptionSerializer(serializers.ModelSerializer):
    '''serialize option objects'''
    class Meta:
        model = Option
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    '''serialize student objects'''
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = "__all__"

