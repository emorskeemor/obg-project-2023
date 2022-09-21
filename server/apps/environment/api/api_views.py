from rest_framework import viewsets, generics, permissions, response, status, exceptions
from rest_framework.decorators import action

from .serializers import RoomSerializer, RoomJoinSerializer

from apps.environment.models import Room
from apps.students.models import Student
from apps.environment.api.permissions import RoomAccessPermission

from django.shortcuts import get_object_or_404



class RoomView(generics.RetrieveAPIView):
    '''View for viewing the details about a room'''
    serializer_class = RoomSerializer
    permission_classes = [RoomAccessPermission]

    def get_object(self):
        print("ghsgdssd")
        return super().get_object()


    def retrieve(self, request, pk, *args, **kwargs):
        print("dadasd")
        code = self.request.GET.get("code")
        domain = self.request.GET.get("domain")
        obj = get_object_or_404(
            Room, code=code, domain=domain)
        self.check_object_permissions(self.request, obj)
        # return super().retrieve(request, *args, **kwargs)    
        serialized = self.serializer_class(obj)
        return response.Response(serialized.data, status=status.HTTP_200_OK)

# Viewsets

def get_domain(request)->str:
    domain = request.GET.get("domain", None)
    if domain is None:
        raise exceptions.ValidationError({"error":"domain name was not provided as a url parameter"})
    return domain

class RoomViewSet(viewsets.ModelViewSet):
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
