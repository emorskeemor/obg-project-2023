from rest_framework.serializers import ModelSerializer

from apps.generator.models import Block, OptionBlocks, InsertTogether
from apps.students.api.serializers import OptionSerializer
from apps.environment.api.serializers import RoomSerializer, SettingsSerializer


class OptionBlocksSerializer(ModelSerializer):
    '''serialize option block objects'''
    room = RoomSerializer(read_only=True)
    
    class Meta:
        model = OptionBlocks
        fields = "__all__"
        
class BlockSerializer(ModelSerializer):
    '''serialize block objects'''
    options = OptionSerializer(many=True, read_only=True)
    blocks = OptionBlocksSerializer(read_only=True)
    
    class Meta:
        model = Block
        fields = "__all__"
        
class InsertTogetherSerializer(ModelSerializer):
    '''serialize insert together objects'''
    target = OptionSerializer(read_only=True)
    settings = SettingsSerializer(read_only=True)
    targets = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = InsertTogether
        fields = "__all__"