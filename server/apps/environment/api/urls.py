from django.urls import path

from .api_views import RoomViewSet

from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()
router.register(r'v', RoomViewSet, basename="rooms")

urlpatterns += router.urls