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

class StudentDumpSerializer(serializers.Serializer):
    '''
    serialize data to dump student options via csv
    '''
    options_using = serializers.CharField(
        help_text="the title of the options that is to be used"
        )
    room_code = serializers.CharField(
        help_text="code of the room where the students' data will be dumped"
    )
    generate_dummy_names = serializers.BooleanField(
        default=True,
        help_text="defines if each line in the csv will be given dummy names"
    )
    max_opts_per_student = serializers.IntegerField(
        default=4, required=False,
        label="max options that a student can take"
        )
    allowed_reserves = serializers.IntegerField(default=2, required=False)
    data = serializers.FileField(write_only=True, required=False)
    