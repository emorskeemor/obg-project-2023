from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views import UserViewSet

urlpatterns = [
    
]

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")


urlpatterns += router.urls