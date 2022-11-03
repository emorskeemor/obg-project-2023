from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import response, status

from blocks.core.generate.utility import Generator

from .serializers import (
    OptionBlocksSerializer,
    BlockSerializer,
    InsertTogetherSerializer,
)

from apps.generator.models import (
    OptionBlocks,
    Block,
    InsertTogether,
)

from functools import partial

class GeneratorViewSet(ViewSet):
    
    @action(detail=False, methods=["post"])
    def run(self, request):
        # shortcut
        get = partial(request.POST.get, default=None)   
        
        return response.Response({"data":"successs"}, status=status.HTTP_200_OK)
    
class OptionBlockViewset(ModelViewSet):
    
    permission_classes = [AllowAny]
    serializer_class = OptionBlocksSerializer
    queryset = OptionBlocks.objects.all()
    
class BlockViewset(ModelViewSet):
    
    permission_classes = [AllowAny]
    serializer_class = BlockSerializer
    queryset = Block.objects.all()
    
class InsertTogetherViewset(ModelViewSet):
    
    permission_classes = [AllowAny]
    serializer_class = InsertTogether
    queryset = InsertTogether.objects.all()