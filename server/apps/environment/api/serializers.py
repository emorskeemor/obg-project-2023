from rest_framework import serializers

from apps.environment.models import Room

class RoomSerializer(serializers.ModelSerializer):

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
