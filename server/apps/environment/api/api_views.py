from apps.environment.api.permissions import RoomAccessPermission
from apps.environment.models import (
    Room, 
    GenerationSettings, 
    AvalilableOptionChoices,
    AvailableOption
    )
from apps.students.models import Student

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import (
    exceptions, permissions, 
    response, status, viewsets
    )
from rest_framework.decorators import action

from .serializers import (
    RoomSerializer,
    JoinRoomSerializer,
    SettingsSerializer,
    AvailableOptionChoiceSerializer,
    AvailableOptionSerializer,
    OptionSerializer
)

from .pagination import AvailableOptionPagination

def get_domain(request)->str:
    domain = request.GET.get("domain", None)
    if domain is None:
        raise exceptions.ValidationError({"detail":"domain name was not provided as a url parameter"})
    return domain

class RoomViewSet(viewsets.ModelViewSet):
    '''
    views to view rooms and join them
    '''
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, RoomAccessPermission]

    def retrieve(self, request, pk):
        room = get_object_or_404(
            Room, code=pk, domain=get_domain(request)
            )
        self.check_object_permissions(self.request, room)
        serialized = self.serializer_class(room)
        return response.Response(serialized.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"])
    def join(self, request):
        '''
        Allow a student to join a room
        '''
        serialized = JoinRoomSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        cleaned_get = serialized.data.get
        
        room = get_object_or_404(
            Room, 
            code=cleaned_get("code"),
            domain=cleaned_get("domain")
            )
        # check permissions and ensure room is public for joining
        self.check_object_permissions(request, room)
        if room.public is False:
            return response.Response(
                {"detail":"room is currently unavailable"}, status=status.HTTP_403_FORBIDDEN
                )
        email = cleaned_get("email")
        # validate the email domain matches requirement
        if room.email_domain:
            _, domain = email.split("@")
            if domain != room.email_domain:
                raise exceptions.ValidationError(
                    {"detail":"domain email given did not match required domain name for the room"}
                )
        # if the student already exists in the room, just return the student
        existing = Student.objects.filter(room=room, email=email)
        if existing.exists():
            return response.Response(
                {"student_uuid":get_object_or_404(existing, email=email).uuid}, 
                status=status.HTTP_200_OK
            )
        # create the new student as they don't already exist
        new_student = Student(
            room=room, 
            email=email, 
            first_name=cleaned_get("first_name"),
            last_name=cleaned_get("last_name")
            )
        new_student.save()
        return response.Response({"student_uuid":new_student.uuid}, status=status.HTTP_200_OK)    
        
    def create(self, request):
        # overide create to ensure a pair of settings is also created with the room
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        settings_title = request.data.get("settings_title")
        if settings_title is None:
            raise exceptions.ValidationError({"detail":"title of settings is required"})
        serialized.save(admin=request.user, settings_title=settings_title)
        return response.Response({"detail":"success"}, status=status.HTTP_200_OK)
        

class SettingsViewset(viewsets.ModelViewSet):
    '''
    views to access settings
    '''
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SettingsSerializer
    queryset = GenerationSettings.objects.all()
    
class AvailableOptionChoicesViewset(viewsets.ModelViewSet):
    '''
    views to access available options per room
    '''
    serializer_class = AvailableOptionChoiceSerializer
    queryset = AvalilableOptionChoices.objects.all()
    pagination_class = AvailableOptionPagination
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=["get"], url_path="room-choices")
    def available_room_choices(self, request):
        get = request.GET.get
        room = get_object_or_404(
            Room,
            domain=get("domain"),
            code=get("code")
        )
        queryset = room.options_using.options.order_by("title").all()
        serialized = OptionSerializer(queryset, many=True)
        
        return response.Response(serialized.data)
            
class AvailableOptionViewset(viewsets.ModelViewSet):
    '''
    views to access available option that is linked to available option choices
    '''
    serializer_class = AvailableOptionSerializer
    queryset = AvailableOption.objects.all() 
    permission_classes = [permissions.IsAuthenticated]