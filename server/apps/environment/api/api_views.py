from apps.environment.api.permissions import RoomAccessPermission
from apps.environment.models import (
    Room, 
    GenerationSettings, 
    AvalilableOptions
    )
from apps.students.models import Student

from django.shortcuts import get_object_or_404
from rest_framework import (exceptions, permissions, response,
                            status, viewsets)
from rest_framework.decorators import action

from .serializers import (
    RoomSerializer,
    RoomJoinSerializer,
    SettingsSerializer,
    AvailableOptionsSerializer,
)

# Viewsets

def get_domain(request)->str:
    domain = request.GET.get("domain", None)
    if domain is None:
        raise exceptions.ValidationError({"error":"domain name was not provided as a url parameter"})
    return domain

class RoomViewSet(viewsets.ModelViewSet):
    '''views to view rooms and join them'''
    permission_classes = [permissions.AllowAny]
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    lookup_field = "code"

    def retrieve(self, request, code, *args, **kwargs):
        room = get_object_or_404(
            Room, code=code, domain=get_domain(request))
        self.check_object_permissions(self.request, room)
        serialized = self.serializer_class(room)
        return response.Response(serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def join(self, request):
        '''
        join a room
        '''
        serialized = RoomJoinSerializer(data=request.data)
        if serialized.is_valid():
            code = serialized.data.get("code")
            # get the room
            room = get_object_or_404(
                Room, 
                code=code,
                domain=serialized.data.get("domain")
                )
            email = serialized.data.get("email")
            # if the student already exists in the room, deny access
            if Student.objects.filter(room=room, email=email).exists():
                return response.Response(
                    {"detail":"A user with this email is already registered to this room"}, 
                    status=status.HTTP_403_FORBIDDEN
                    )
            
            new_student = Student(
                room=room, 
                email=email, 
                first_name=serialized.data.get("first_name"),
                last_name=serialized.data.get("last_name")
                )

            new_student.save()
            return response.Response(
                {"student_uuid":new_student.uuid}, 
                status=status.HTTP_200_OK
                )
        # only return the first error
        first_error = tuple(serialized.errors.values())[0][0]
        return response.Response(
            {"detail": first_error}, status=status.HTTP_400_BAD_REQUEST
            )

class SettingsViewset(viewsets.ModelViewSet):
    '''views to access settings'''
    permission_classes = [permissions.AllowAny]
    serializer_class = SettingsSerializer
    queryset = GenerationSettings.objects.all()
    
class AvailableOptionsViewset(viewsets.ModelViewSet):
    '''views to access available options per room'''
    permission_classes = [permissions.AllowAny]
    serializer_class = AvailableOptionsSerializer
    queryset = AvalilableOptions.objects.all()