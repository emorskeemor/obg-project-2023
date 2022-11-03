from django.urls import path

from .api_views import GeneratorViewSet

from rest_framework.routers import DefaultRouter


urlpatterns = [
    
]

router = DefaultRouter()

router.register(r"u", GeneratorViewSet, basename="generator")


urlpatterns +=  router.urls