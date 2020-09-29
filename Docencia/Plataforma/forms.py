from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from .models import *
from django.utils.translation import gettext_lazy as _

__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"

from Docencia.Plataforma.models import Class

class ClassForm(forms.ModelForm):    
    class Meta:
        model = Class
        fields = ("subject", "name", "body", "datepub", "resources")
        labels = {
            "subject": "Asignatura",
            "name": "Título",
            "body": "Cuerpo",
            "datepub": "Fecha de Publicación",
            "resources": "Recursos"
        }



