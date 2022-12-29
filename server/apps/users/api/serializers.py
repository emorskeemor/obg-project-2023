from rest_framework import serializers

from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ("uuid","email", "password", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user 
