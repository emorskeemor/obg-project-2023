from rest_framework import permissions

class RoomAccessPermission(permissions.BasePermission):
    message = 'Access denied'

    def has_object_permission(self, request, view, obj, *args, **kwargs):
        user = getattr(obj, "admin", None)
        return user == request.user