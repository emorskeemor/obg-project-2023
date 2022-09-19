from rest_framework import views, generics, permissions
from .serializers import RoomSerializer

from apps.environment.models import Room
from apps.environment.api.permissions import RoomAccessPermission

from django.shortcuts import get_object_or_404



class RoomView(generics.RetrieveAPIView):
    '''View for viewing the details about a room'''
    serializer_class = RoomSerializer
    permission_classes = [RoomAccessPermission]

    def get_object(self):
        code = self.request.GET.get("code")
        domain = self.request.GET.get("domain")
        obj = get_object_or_404(
            Room, code=code, domain=domain)
        self.check_object_permissions(self.request, obj)
        return obj        