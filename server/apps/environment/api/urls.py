from django.urls import path

from .api_views import (
    RoomViewSet, 
    SettingsViewset,
    AvailableOptionChoicesViewset, 
    AvailableOptionViewset
    )

from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename="rooms")
router.register(r'available-option-choices', AvailableOptionChoicesViewset, basename="available-option-choices")
router.register(r'available-options', AvailableOptionViewset, basename="available-option")
router.register(r'settings', SettingsViewset, basename="settings")

urlpatterns += router.urls