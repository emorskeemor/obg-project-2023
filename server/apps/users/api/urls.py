from django.urls import path
from .api_views import TestApiView

urlpatterns = [
    path("test/", TestApiView.as_view(), name="test-view")
]