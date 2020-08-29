from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib import admin

from Docencia.Cursos.models import CourseInformation

class Class(models.Model):
    """Model definition for Class."""
    course = models.ForeignKey("Docencia.CourseInformation", verbose_name="Curso", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Nombre", max_length=100)
    body=CKEditor5Field('Cuerpo', config_name='extends')
    uploaddate = models.DateField('Fecha Creación', auto_now=True)
    datepub = models.DateTimeField('Fecha Pub.', auto_now=False, auto_now_add=False)

    class Meta:
        """Meta definition for Class."""
        verbose_name = 'Clase'
        verbose_name_plural = 'Plataforma - Clases'

    def __str__(self):
        """Unicode representation of Class."""
        return "%s %s (%s)" % (self.course, self.name, self.uploaddate)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    '''Admin View for Class'''
    list_display = ('course', 'name', 'uploaddate', 'datepub')
    list_filter = ('course',)
    search_fields = ('course__name', 'course__sede__name')
    ordering = ('-uploaddate',)
    readonly_fields = ('uploaddate',)