from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from .models import *
from django.utils.translation import gettext_lazy as _

from captcha.fields import ReCaptchaField

__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"

from Docencia.DatosPersonales.models import *

class StudentPersonalInformationForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = StudentPersonalInformation

        fields = ["name", "lastname", "gender", "numberidentification", "nacionality", 
                  "street", "city", "state", "cellphone", "phone", "email", "degree", 
                  "title", "ocupation"]

        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'José María',
                'autofocus': 'on'
                
            }),
            "lastname": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pérez Pérez',
                
            }),
            "numberidentification": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de Carnet',
                'pattern': '[0-9]{11}',
                'minlength': 11,
                'maxlength': 11,
                
            }),
            "gender": forms.Select(attrs={
                'class': 'form-label-group form-select form-select-md'
            }),
            "street": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '23 Nº 328 entre L y M',                
            }),
            "city": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Plaza de la Revolución',                
            }),
            "state": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'La Habana',
                'value': 'La Habana',                
            }),
            "cellphone": forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'phone',
                'placeholder': '53891457',                
            }),
            "phone": forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'phone',
                'placeholder': '77662418',                
            }),
            "email": forms.EmailInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'joseperezperez@example.com',
            }),
            "nacionality": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'cubana',
            }),
            "degree": forms.Select(attrs={
                'class': 'form-label-group form-select form-select-md'
            }),
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del Estudiante',
                
            }),
            "ocupation": forms.Select(attrs={
                'class': 'form-label-group form-select form-select-md'
            }),
        }

        labels = {
            "name": _("Nombre"),
            "lastname": _("Apellidos"),
            "gender": _("Género"),
            "numberidentification": _("CI"),
            "street": _("Calle"),
            "city": _("Municipio"),
            "state": _("Provincia"),
            "cellphone": _("Móvil"),
            "phone": _("Teléfono"),
            "email": _("E-mail"),
            "image": _("Foto Perfil"),
            "nacionality": _("Nacionalidad"),
            "degree": _("Grado Científico"),
            "title": _("Título"),
            "ocupation": _("Ocupación")
        }

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Este estudiante ya existe.",
                'numberidentification': "Este Número de Identificación ya está existe"
            }
        }
# <> fin StudentPersonalInformationForm
