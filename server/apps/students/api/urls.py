from django.urls import path
from rest_framework.routers import DefaultRouter

from .viewsets import ChoiceViewset, OptionViewset, StudentViewset, RequirementViewSet

urlpatterns = []

router = DefaultRouter()
# default viewsets for testing
router.register(r"u", StudentViewset, basename="students")
router.register(r"c", ChoiceViewset, basename="choices")
router.register(r"o", OptionViewset, basename="options")
router.register(r"r", RequirementViewSet, basename="requirements")



urlpatterns += router.urls