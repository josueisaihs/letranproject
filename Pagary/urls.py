from django.urls import path
from . import views

__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"


urlpatterns = [
    path("", views.pagary, name="pagary")
]