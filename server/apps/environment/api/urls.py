from django.urls import path

from .api_views import (
    RoomViewSet, 
    AvailableOptionsViewset, 
    SettingsViewset
    )

from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()
router.register(r'r', RoomViewSet, basename="rooms")
router.register(r'o', AvailableOptionsViewset, basename="available-options")
router.register(r's', SettingsViewset, basename="settings")

urlpatterns += router.urls