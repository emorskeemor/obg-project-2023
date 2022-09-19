from django.urls import path
from .api_views import RoomView
urlpatterns = [
    path("view/", RoomView.as_view(), name="room-view")
]