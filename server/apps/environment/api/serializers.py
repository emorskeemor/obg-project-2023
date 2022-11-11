from rest_framework import serializers

from apps.environment.models import (
    Room, 
    AvalilableOptionChoices, 
    GenerationSettings, 
    AvailableOption
    )

from apps.students.api.serializers import OptionSerializer

class RoomSerializer(serializers.ModelSerializer):
    '''
    serialize room objects
    '''
    class Meta:
        model = Room
        fields = "__all__"

    
class RoomJoinSerializer(serializers.Serializer):
    '''
    serializer for validating a student joining a room
    '''
    code = serializers.CharField(max_length=8)
    domain = serializers.CharField(max_length=50)
    email = serializers.EmailField()

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

class AvailableOptionChoiceSerializer(serializers.ModelSerializer):
    '''
    serialize avaliable option objects
    '''
    room = RoomSerializer(read_only=True)
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = AvalilableOptionChoices
        fields = "__all__"        
        
class AvailableOptionSerializer(serializers.ModelSerializer):
    '''
    serialize a single available option
    '''
    option = OptionSerializer(read_only=True)
    option_choices = AvailableOptionChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = AvailableOption
        fields = "__all__"
        
class SettingsSerializer(serializers.ModelSerializer):
    '''
    serialize settings objects
    '''
    room = RoomSerializer(read_only=True)
    
    class Meta:
        model = GenerationSettings
        fields = "__all__"