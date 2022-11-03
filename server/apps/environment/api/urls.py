from django.urls import path

from .api_views import (
    RoomViewSet, 
    AvailableOptionsViewset, 
    SettingsViewset
    )

from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename="rooms")
router.register(r'opts', AvailableOptionsViewset, basename="available-options")
router.register(r'settings', SettingsViewset, basename="settings")

urlpatterns += router.urls