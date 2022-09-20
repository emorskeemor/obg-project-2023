from django.urls import path

from .api_views import RoomView, RoomViewSet

from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path("view/", RoomView.as_view(), name="room-view"),
]

router = DefaultRouter()
router.register(r'v', RoomViewSet, basename="rooms")

urlpatterns += router.urls