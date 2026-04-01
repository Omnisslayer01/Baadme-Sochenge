from django.urls import path
from . import views

urlpatterns = [
    path("home/",views.flashlight_tasks, name="home"),
    path("update_task/" , views.update_task , name = "update_task"),
    path("waifu/", views.waifu_chat , name = "user_response"),

]