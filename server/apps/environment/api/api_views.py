from apps.environment.api.permissions import RoomAccessPermission
from apps.environment.models import (
    Room, 
    GenerationSettings, 
    AvalilableOptionChoices,
    AvailableOption,
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
from apps.students.models import Option

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
    permission_classes = [RoomAccessPermission]

    def retrieve(self, request, pk):
        room = get_object_or_404(Room, code=pk)
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
        if room.public is False:
            return response.Response(
                {"detail":"room is currently unavailable"}, status=status.HTTP_403_FORBIDDEN
                )
        email = cleaned_get("email")
        # validate the email domain matches requirement
        if room.email_domain and room.check_email_domain:
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
    
    @action(detail=True, methods=["get"])
    def room_available(self, request, pk): 
        room = get_object_or_404(Room, code=pk, domain=get_domain(request))
        if room.public:
            return response.Response({"detail":"room is public and can be accessed"}, status=status.HTTP_200_OK)
        return response.Response({"detail":"room is private and cannot be accessed"}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=True, methods=["get"])
    def room_with_settings(self, request, pk):
        room = get_object_or_404(Room, code=pk)
        room_serialized = self.serializer_class(room)
        # add the settings of the room as well
        settings = get_object_or_404(GenerationSettings, room=room)
        available_opts = get_object_or_404(AvalilableOptionChoices, room=room)
        payload = {}
        settings_serialized = SettingsSerializer(settings)
        settings_data = settings_serialized.data.copy()
        settings_data.pop("room")
        payload["room"] = room_serialized.data
        payload["settings"] = settings_data
        payload["opts_id"] = available_opts.pk
        return response.Response(payload, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"])
    def retrieve_using_domain_and_code(self, request):
        get = request.data.get
        room = get_object_or_404(Room, domain=get("domain"), code=get("code"))
        serialized = self.serializer_class(room)
        return response.Response(serialized.data, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=["get"], url_path="available-options")
    def available_options(self, request, pk):
        room = get_object_or_404(Room, code=pk)
        room_opts = get_object_or_404(AvalilableOptionChoices, room=room)
        opts = room_opts.options.all().order_by("title")
        all_opts = []
        all_available_opts = Option.objects.all().order_by("title")
        for available in all_available_opts:
            if not opts.filter(pk=available.pk).exists():
                all_opts.append(available)
        payload = {}
        room_opts_serialized = OptionSerializer(opts, many=True)
        all_opts_serializeed = OptionSerializer(all_opts, many=True)
        payload["room"] = room_opts_serialized.data
        payload["all"] = all_opts_serializeed.data 
        return response.Response(payload, status=status.HTTP_200_OK)
         
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
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=["get"], url_path="room-choices")
    def available_room_choices(self, request):
        get = request.GET.get
        room = get_object_or_404(
            Room,
            domain=get("domain"),
            code=get("code")
        )
        # queryset = room.options_using.options.order_by("title").all()
        available_option_choices = get_object_or_404(AvalilableOptionChoices, room=room)
        queryset = available_option_choices.options.order_by("title").all()
        serialized = OptionSerializer(queryset, many=True)
        
        return response.Response(serialized.data)
    
    @action(detail=True, methods=["put"])
    def batch_update(self, request, pk):
        
        current = get_object_or_404(AvalilableOptionChoices.objects.prefetch_related("options"), pk=pk)
        all_options = Option.objects.all()
        options = request.data.get("options")
        
        new_options = []
        for option in options:
            pk = option.get("id")
            individual = current.options.filter(pk=pk)
            if not individual.exists():
                new_options.append(AvailableOption(option=all_options.get(pk=pk), option_choices=current))
        for current_option in AvailableOption.objects.filter(option_choices=current):
            found = False
            for option in options:
                if option.get("id") == current_option.option.pk:
                    found = True
                    break
            if not found:
                current_option.delete()
                
        AvailableOption.objects.bulk_create(new_options)
        return response.Response(status=status.HTTP_200_OK)
            
class AvailableOptionViewset(viewsets.ModelViewSet):
    '''
    views to access available option that is linked to available option choices
    '''
    serializer_class = AvailableOptionSerializer
    queryset = AvailableOption.objects.all() 
    permission_classes = [permissions.IsAuthenticated]