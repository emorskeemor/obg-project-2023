from rest_framework import permissions

from apps.environment.models import Room

class RoomAccessPermission(permissions.BasePermission):
    message = 'You do not have access to this Room'

    def has_object_permission(self, request, view, obj):
        assert isinstance(obj, Room), "object to check must be an instance of a room and not '%s'" % obj
        return obj.admin == request.user