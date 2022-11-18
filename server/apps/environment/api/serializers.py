from rest_framework import serializers

from apps.environment.models import (
    Room, 
    AvalilableOptionChoices, 
    GenerationSettings, 
    AvailableOption,

    )
from apps.users.api.serializers import UserSerializer
from apps.students.api.serializers import OptionSerializer

class RoomSerializer(serializers.ModelSerializer):
    '''
    serialize room objects
    '''    
    code = serializers.CharField(max_length=8, help_text="room code", read_only=True)
    domain = serializers.CharField(max_length=50, help_text="room domain name")
    title = serializers.CharField()
    admin = UserSerializer(required=False)
    public = serializers.BooleanField(help_text="determines if the room can be accessed", required=False)
    
    class Meta:
        model = Room
        fields = ["code","domain","title", "admin", "public", "pk", "email_domain", "check_email_domain"]
        
    def create(self, validated_data):
        settings_title = validated_data.pop("settings_title")
        assert settings_title, "'settings_title' must be passed to save() method for settings model"
        new_room = Room.objects.create(**validated_data)
        AvalilableOptionChoices.objects.create(
            title="default-available-opts",
            room=new_room
        )
        GenerationSettings.objects.create(
            room=new_room, 
            title=settings_title
            )
        return new_room
        
                
class JoinRoomSerializer(serializers.Serializer):
    '''
    serializer for validating a student joining a room
    '''
    code = serializers.CharField(max_length=8, help_text="room code")
    domain = serializers.CharField(max_length=50, help_text="room domain name")
    # for student
    email = serializers.EmailField(help_text="student email")
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)

class AvailableOptionChoiceSerializer(serializers.ModelSerializer):
    '''
    serialize avaliable option objects
    '''
    title = serializers.CharField(max_length=50)
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = AvalilableOptionChoices
        fields = ["title", "options", "pk"]        

class AvailableOptionSerializer(serializers.ModelSerializer):
    '''
    serialize a single available option
    '''
    option = OptionSerializer(read_only=True)
    option_choices = AvailableOptionChoiceSerializer(many=True, read_only=True)
    classes = serializers.IntegerField(help_text="classes delegated to this subject")
    class Meta:
        model = AvailableOption
        fields = ["option", "option_choices", "classes", "pk"]
        
class SettingsSerializer(serializers.ModelSerializer):
    '''
    serialize settings objects
    '''
    room = RoomSerializer(read_only=True, help_text="room connected to")
    title = serializers.CharField(help_text="name of settings")
    blocks_must_align = serializers.BooleanField(
        help_text="defines that the blocks must be of equal length"
    )
    max_subjects_per_block = serializers.IntegerField(
        help_text="maximum number of subjects per block"
        )
    blocks = serializers.IntegerField(help_text="number of available blocks")
    class_size = serializers.IntegerField(help_text="the max number of students per class")
    lesson_cost = serializers.FloatField(help_text="cost per lesson (£)")
    
    class Meta:
        model = GenerationSettings
        fields = "__all__"