from django import forms

from Docencia.Index.models import Recurso

class RecursoForm(forms.ModelForm):    
    class Meta:
        model = Recurso
        fields = ("name", "recurso", "tipo", "courses")
