from django.urls import path
from . import views

urlpatterns = [
    path("home/",views.flashlight_tasks, name="home")
]