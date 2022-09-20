from rest_framework.routers import DefaultRouter

from django.urls import path

from .viewsets import StudentViewset, OptionViewset, ChoiceViewset

urlpatterns = []

router = DefaultRouter()
# default viewsets for testing
router.register(r"u", StudentViewset, basename="students")
router.register(r"c", ChoiceViewset, basename="choices")
router.register(r"o", OptionViewset, basename="options")



urlpatterns += router.urls