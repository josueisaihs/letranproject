from django import forms
from django_ckeditor_5.fields import CKEditor5Field

from Docencia.Plataforma.models import Class
import json


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
