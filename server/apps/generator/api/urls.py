from django.urls import path

from .api_views import (
    GerneratorViewset,
    OptionBlockViewset,
    BlockViewset,
    InsertTogetherViewset,
    )

from rest_framework.routers import DefaultRouter

urlpatterns = [
    
]

router = DefaultRouter()

router.register(r"generator", GerneratorViewset, basename="generator")
router.register(r"option-blocks", OptionBlockViewset, basename="option-blocks")
router.register(r"blocks", BlockViewset, basename="block")
router.register(r"together", InsertTogetherViewset, basename="together")


urlpatterns +=  router.urls