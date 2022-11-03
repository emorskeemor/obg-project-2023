from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import response, status

from blocks.core.generate.utility import Generator

from functools import partial

class GeneratorViewSet(ViewSet):
    
    @action(detail=False, methods=["post"])
    def run(self, request):
        # short cut
        get = partial(request.POST.get, default=None)
        
        # settings
        # gen = Generator(
            
        # )
        # gen.prepare_generation()
        
        
        
        
        
        return response.Response({"data":"successs"}, status=status.HTTP_200_OK)