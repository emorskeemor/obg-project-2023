from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

from apps.users.models import User

from apps.environment.models import Room
from apps.environment.api.serializers import RoomSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from core.utils import valid_uuid_or_error

class UserViewSet(ModelViewSet):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=["get"])
    def rooms(self, request, pk):
        valid_uuid_or_error(pk)
        user = get_object_or_404(
            get_user_model(), 
            uuid=pk
            )
        rooms = Room.objects.filter(admin=user)
        serialized = RoomSerializer(rooms, many=True)
        
        return Response(serialized.data, status=status.HTTP_200_OK)