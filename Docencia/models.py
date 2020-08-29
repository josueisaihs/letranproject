from django.db import models
from django.contrib.admin import ModelAdmin

# Create your models here.
import Docencia.DatosPersonales.models as datospersonales
import Docencia.Cursos.models as cursos
import Docencia.Admision.models as admision
import Docencia.Index.models as index
import Docencia.Plataforma.models as plataforma

class RespuestasError(models.Model):
    """Model definition for RespuestasError."""
    autor = models.CharField(max_length=100, verbose_name="Autor", default="Yo")
    body = models.CharField(max_length=300, verbose_name="Texto")

    class Meta:
        """Meta definition for RespuestasError."""

        verbose_name = 'Respuesta a Error'
        verbose_name_plural = 'Index - Respuestas a Error'

    def __str__(self):
        """Unicode representation of RespuestasError."""
        return "%s - %s" % (self.autor, self.body)

    class Admin(ModelAdmin):    
        list_display = ('autor', 'body',)
        search_fields = ('autor', 'body',)
