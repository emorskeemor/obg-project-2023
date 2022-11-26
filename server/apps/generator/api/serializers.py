from rest_framework import serializers

from apps.generator.models import Block, OptionBlocks, InsertTogether
from apps.students.api.serializers import OptionSerializer
from apps.environment.api.serializers import RoomSerializer, SettingsSerializer


class OptionBlocksSerializer(serializers.ModelSerializer):
    '''
    serialize option block objects
    '''
    room = RoomSerializer(read_only=True)
    title = serializers.CharField(max_length=50)
    number_of_blocks = serializers.IntegerField()
    
    class Meta:
        model = OptionBlocks
        fields = "__all__"
        
class BlockSerializer(serializers.ModelSerializer):
    '''
    serialize a single block object
    '''
    options = OptionSerializer(many=True, read_only=True)
    blocks = OptionBlocksSerializer(read_only=True)
    
    class Meta:
        model = Block
        fields = "__all__"
        
class InsertTogetherSerializer(serializers.ModelSerializer):
    '''
    serialize insert together objects
    '''
    target = OptionSerializer(read_only=True)
    settings = SettingsSerializer(read_only=True)
    targets = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = InsertTogether
        fields = ["target", "settings", "targets", "pk"]
        
class GenerationSerializer(serializers.Serializer):
    '''
    serialize post data before running generator
    '''
    # settings_title = serializers.CharField(
    #     help_text= (
    #         "name of the settings that is to be used. This needs to point to "
    #         "a set of settings that is linked to the given room code"
    #         )
    # )
    code = serializers.CharField(max_length=8, help_text="room code")
    # domain = serializers.CharField(max_length=50, help_text="room domain name")
    # options_title = serializers.CharField(
    #     help_text=(
    #         "the name of the set of available options. This needs to point to "
    #         "a set of 'availalble_option_choices' that have exist in the database"
    #     )
    # )
    
    data_using_csv = serializers.BooleanField(default=False, required=False)
    subjects_using_csv = serializers.BooleanField(default=False, required=False)
    
    data = serializers.FileField(
        help_text="data csv file if not using database",
        write_only=True,
    )
    options = serializers.FileField(
        help_text="available options file if not using database",
        write_only=True,
    )
    