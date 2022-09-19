# rest
from rest_framework import generics, views, status
from rest_framework.response import Response

class TestApiView(views.APIView):
    '''testing endpoint'''
    def get(self, request, *args, **kwargs):
        return Response({"message":"endpoint successful"}, status=status.HTTP_200_OK )
