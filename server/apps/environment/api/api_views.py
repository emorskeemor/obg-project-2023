from apps.environment.api.permissions import RoomAccessPermission
from apps.environment.models import (
    Room, 
    GenerationSettings, 
    AvalilableOptionChoices,
    AvailableOption
    )
from apps.students.models import Student

from django.shortcuts import get_object_or_404

from rest_framework import (
    exceptions, permissions, 
    response, status, viewsets
    )
from rest_framework.decorators import action

from .serializers import (
    RoomSerializer,
    RoomJoinSerializer,
    SettingsSerializer,
    AvailableOptionChoiceSerializer,
    AvailableOptionSerializer,
    OptionSerializer
)

from .pagination import AvailableOptionSerializer


# Viewsets

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
        allow a student to join a room
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
            _, domain = email.split("@")
            if domain != room.email_domain:
                raise exceptions.ValidationError(
                    {"detail":"domain email did not match required domain name"}
                )
            # if the student already exists in the room, deny access
            existing = Student.objects.filter(room=room, email=email)
            if existing.exists():
                return response.Response(
                    {"student_uuid":get_object_or_404(existing, email=email).uuid}, 
                    status=status.HTTP_200_OK
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
    '''
    views to access settings
    '''
    serializer_class = SettingsSerializer
    queryset = GenerationSettings.objects.all()
    
class AvailableOptionChoicesViewset(viewsets.ModelViewSet):
    '''
    views to access available options per room
    '''
    serializer_class = AvailableOptionChoiceSerializer
    queryset = AvalilableOptionChoices.objects.all()
    pagination_class = AvailableOptionSerializer
    
    @action(detail=False, methods=["get"], url_path="room-choices")
    def available_room_choices(self, request):
        get = request.GET.get
        room = get_object_or_404(
            Room,
            domain=get("domain"),
            code=get("code")
        )
        queryset = room.options_using.options.order_by("title").all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OptionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OptionSerializer(queryset, many=True)
        return response.Response(serializer.data)
    
class AvailableOptionViewset(viewsets.ModelViewSet):
    '''
    views to access available option that is 
    linked to available option choices
    '''
    serializer_class = AvailableOptionSerializer
    queryset = AvailableOption.objects.all() 