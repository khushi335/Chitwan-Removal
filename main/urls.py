from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path("about",about,name="about"),
    path("services",services,name="services"),
    path("appliances",appliances,name="appliances"),
    path("contact",contact,name="contact"),
]