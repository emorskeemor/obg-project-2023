from apps.environment.api.permissions import RoomAccessPermission
from apps.environment.models import (
    Room, 
    GenerationSettings, 
    AvalilableOptionChoices,
    AvailableOption,
    )
from apps.students.models import Student

from django.shortcuts import get_object_or_404

from rest_framework import (
    exceptions, permissions, 
    response, status, viewsets
    )
from rest_framework.decorators import action
from rest_framework.request import Request

from .serializers import (
    RoomSerializer,
    JoinRoomSerializer,
    SettingsSerializer,
    AvailableOptionChoiceSerializer,
    AvailableOptionSerializer,
    OptionSerializer,
)
from apps.students.models import Option
from apps.generator.models import InsertTogether, OptionBlocks
from apps.generator.api.serializers import OptionBlocksSerializer
from apps.generator.api.serializers import InsertTogetherSerializer

from .pagination import AvailableOptionPagination

from typing import List, Dict, Any

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
    def join(self, request: Request):
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
            # TODO THIS WILL BREAK IF MULTIPLE @ signs are PRESENT
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
        '''
        returns response whether or not the room is available or closed
        '''
        room = get_object_or_404(Room, code=pk, domain=get_domain(request))
        if room.public:
            return response.Response({"detail":"room is public and can be accessed"}, status=status.HTTP_200_OK)
        return response.Response({"detail":"room is private and cannot be accessed"}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=True, methods=["get"], url_path="room-with-settings")
    def room_with_settings(self, request, pk):
        '''
        return details about a room and its settings that are attached to it
        '''
        room = get_object_or_404(Room, code=pk)
        room_serialized = self.serializer_class(room)
        # get the settings, available options and the insertion rules
        # for the room too
        settings = get_object_or_404(GenerationSettings, room=room)
        available_opts = get_object_or_404(AvalilableOptionChoices, room=room)
        insertions = InsertTogether.objects.filter(settings=settings)
        # serialize everything we need
        settings_serialized = SettingsSerializer(settings)
        inserts_serialized = InsertTogetherSerializer(insertions, many=True)
        settings_data = settings_serialized.data.copy()
        settings_data.pop("room")
        # serialize the option blocks by ONLY providing the subject code and its title
        blocks = OptionBlocks.objects.filter(room=room)
        rooms_option_blocks = []
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
            serialized_data = serialized_opt_blocks.data.copy()
            serialized_data["blocks"] = opt_block_codes
            rooms_option_blocks.append(serialized_data)
            
        payload = {
            "room": room_serialized.data,
            "inserts": inserts_serialized.data,
            "settings": settings_data,
            "opts_id": available_opts.pk,
            "blocks": rooms_option_blocks
        }
        return response.Response(payload, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"])
    def retrieve_using_domain_and_code(self, request: Request):
        '''
        return a room's details by using the domain and room code
        '''
        room = get_object_or_404(
            Room, 
            domain=request.data.get("domain"), 
            code=request.data.get("code")
            )
        serialized = self.serializer_class(room)
        return response.Response(serialized.data, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=["get"], url_path="available-options")
    def available_options(self, request, pk):
        '''
        return all available options for a room
        '''
        room = get_object_or_404(Room, code=pk)
        room_opts = get_object_or_404(AvalilableOptionChoices, room=room)
        current_opts = room_opts.options.all().order_by("title")
        # serialize all the vailable options that the user can pick. Filter out
        # those that already have been chosen. 
        all_opts = []
        all_available_opts = Option.objects.all().order_by("title")
        for available in all_available_opts:
            if not current_opts.filter(pk=available.pk).exists():
                all_opts.append(available)
        all_opts_serializeed = OptionSerializer(all_opts, many=True)
        # serialize the current chosen options
        opts = AvailableOption.objects.filter(option_choices=room_opts)
        room_opts_serialized = AvailableOptionSerializer(opts, many=True)
        room_opts_data = []
        for option in room_opts_serialized.data.copy():
            opt = option.pop("option")
            orignal = opt.pop("title")
            room_opts_data.append({
                "original":orignal,
                **option,
                **opt, 
            })
            
        payload = {
            "room": room_opts_data,
            "all": all_opts_serializeed.data
        }
        return response.Response(payload, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["delete"], url_path="delete-all-students")
    def delete_all_students(self, request: Request, pk):
        '''
        deletes all students from a given room. WARNING: this 
        cannot be undone once comitted
        '''
        room = get_object_or_404(Room, code=pk)
        self.check_object_permissions(request, room)
        for student in Student.objects.filter(room=room):
            student.delete()
        return response.Response({"detail":"all students deleted successfully"}, status=status.HTTP_200_OK )
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
    def available_room_choices(self, request: Request):
        '''
        gets all available options for a given room. Returns 'Option' object
        '''
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
        '''
        batch update available options to either delete them or add new 
        available options to a room.
        '''
        available = get_object_or_404(AvalilableOptionChoices, pk=pk)
        all_options = Option.objects.all()
        options: List[Dict[str, Any]] = request.data.get("options")
        # TODO: need serialization validation
        current = AvailableOption.objects.filter(
            option_choices=available
        )
        # go through the options we have and check if they already exist.
        # if they do not, then create a new one to be bulk created. If they do,
        # then we just need to update them.
        new_options = []
        for option in options:
            pk = option.get("id", None)
            serialized = AvailableOptionSerializer(data=option)
            serialized.is_valid()
            
            classes = serialized.data.get("classes", None)
            title = serialized.data.get("title", None)
            individual = available.options.filter(pk=pk)
            # continue
            if not individual.exists():
                print("creating new")
                # create a new available option
                base = all_options.get(pk=pk)
                new_options.append(
                    AvailableOption(
                        option=base, 
                        option_choices=available,
                        classes=classes,
                        title=base.title
                        )
                    )
            else:
                print("updating previous")
                # update
                to_update = current.filter(option__pk=pk)[0]
                if not classes:
                    classes = None
                to_update.classes = classes
                to_update.title = title
                to_update.save()
                
        # delete any available options if they have been removed.
        for current_option in AvailableOption.objects.filter(option_choices=available):
            found = False
            for option in options:
                if option.get("id") == current_option.option.pk:
                    found = True
                    break
            if not found:
                # TODO: not atomic
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
    
    

