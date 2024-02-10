from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views import (
    ChoiceViewset, 
    OptionViewset, 
    StudentViewset, 
    )

urlpatterns = []

router = DefaultRouter()
# default viewsets for testing
router.register(r"students", StudentViewset, basename="students")
router.register(r"choices", ChoiceViewset, basename="choices")
router.register(r"options", OptionViewset, basename="options")



urlpatterns += router.urls