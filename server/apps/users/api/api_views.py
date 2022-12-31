from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import UserSerializer

from apps.users.models import User
from apps.generator.models import OptionBlocks

from apps.environment.models import Room
from apps.environment.api.serializers import RoomSerializer
from apps.generator.api.serializers import OptionBlocksSerializer, BlockSerializer


from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from core.utils import valid_uuid_or_error

class UserViewSet(ModelViewSet):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()        
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=["get"])
    def rooms(self, request, pk):
        valid_uuid_or_error(pk)
        user = get_object_or_404(
            get_user_model(), 
            uuid=pk
            )
        rooms = Room.objects.filter(admin=user)
        serialized = RoomSerializer(rooms, many=True)
        blocks = OptionBlocks.objects.filter(created_by=request.user)
        serialized_blocks = []
        for option_blocks in blocks:
            serialized_opt_blocks = OptionBlocksSerializer(option_blocks)
            opt_block_codes = []
            for block in option_blocks.blocks.all():
                block_codes = []
                for subject in block.options.all():
                    block_codes.append(
                        (subject.subject_code, subject.title)
                    )
                opt_block_codes.append(block_codes)
            data = serialized_opt_blocks.data.copy()
            data["blocks"] = opt_block_codes
            serialized_blocks.append(data)
        
        payload = {
            "rooms": serialized.data,
            "user": self.serializer_class(user).data,
            "blocks": serialized_blocks
        }
        return Response(payload, status=status.HTTP_200_OK)