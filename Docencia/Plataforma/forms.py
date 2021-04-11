from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from Docencia.Plataforma.models import Class, HomeWork
import json
from captcha.fields import ReCaptchaField


class ClassForm(forms.ModelForm):
    recursosjson = forms.JSONField(
        max_length=1024,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Class
        fields = ('subject', 'name', 'classbody', 'datepub')
        widgets = {            
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Clase X',
                'autofocus': 'on'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-label-group form-select form-select-md d-none'
            }),
            'body': forms.Textarea(attrs={
                'class': 'django_ckeditor_5'
            }),
            'datepub': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#id_datepub_div',
            })
        }

class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ('name', 'clase', 'student', 'file', 'edition')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'clase': forms.HiddenInput(attrs={
                'value': '0'
            }),
            'student': forms.HiddenInput(attrs={
                'value': '0'
            }),
            'edition': forms.HiddenInput(attrs={
                    'value': '0'
            }),
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione un archivo',
                    'autofocus': 'on',
                    'accept': 'application/pdf'
                }
            )
        }

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Esta tarea con este Nombre ya existe.",
            }
        }

class DocForm(forms.Form):
    captcha = ReCaptchaField()
    doc = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Seleccione un archivo',
        'autofocus': 'on',
        'accept': 'application/pdf'
    }))

class PayForm(forms.Form):
    captcha = ReCaptchaField()
    transfernumber = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Numero de Transaccion',
        'autofocus': 'on',
        'pattern': '[A-Za-z0-9]{13}|[0-9]{16}'
    }))

class PayValidatorForm(forms.Form):
    txt = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Mensaje de Transfermovil: Ultimas Operaciones',
        'autofocus': 'on'
    }))
