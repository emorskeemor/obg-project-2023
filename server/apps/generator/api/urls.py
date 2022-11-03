from django.urls import path

from .api_views import (
    GeneratorViewSet,
    OptionBlockViewset,
    BlockViewset,
    InsertTogetherViewset,
    )

from rest_framework.routers import DefaultRouter

urlpatterns = [
    
]

router = DefaultRouter()

router.register(r"u", GeneratorViewSet, basename="generator")
router.register(r"o", OptionBlockViewset, basename="option-blocks")
router.register(r"b", BlockViewset, basename="block")
router.register(r"t", InsertTogetherViewset, basename="together")


urlpatterns +=  router.urls