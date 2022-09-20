from rest_framework.routers import DefaultRouter

from django.urls import path

from .api_views import TestApiView
from .viewsets import UserViewSet

urlpatterns = [
    path("test/", TestApiView.as_view(), name="test-view")
]
router = DefaultRouter()
router.register(r"u", UserViewSet, basename="users")


urlpatterns += router.urls