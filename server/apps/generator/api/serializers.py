from rest_framework import serializers

from apps.generator.models import Block, OptionBlocks, InsertTogether
from apps.students.api.serializers import OptionSerializer
from apps.environment.api.serializers import RoomSerializer, SettingsSerializer


class OptionBlocksSerializer(serializers.ModelSerializer):
    '''serialize option block objects'''
    room = RoomSerializer(read_only=True)
    
    class Meta:
        model = OptionBlocks
        fields = "__all__"
        
class BlockSerializer(serializers.ModelSerializer):
    '''serialize block objects'''
    options = OptionSerializer(many=True, read_only=True)
    blocks = OptionBlocksSerializer(read_only=True)
    
    class Meta:
        model = Block
        fields = "__all__"
        
class InsertTogetherSerializer(serializers.ModelSerializer):
    '''serialize insert together objects'''
    target = OptionSerializer(read_only=True)
    settings = SettingsSerializer(read_only=True)
    targets = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = InsertTogether
        fields = "__all__"
        
class PregenerateSerializer(serializers.Serializer):
    
    settings_title = serializers.CharField()
    room_code = serializers.CharField()
    options_title = serializers.CharField()
    
    data_using_csv = serializers.BooleanField(default=False, required=False)
    subjects_using_csv = serializers.BooleanField(default=False, required=False)
    