from django.db import models
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

import os
from datetime import date, timedelta

from Docencia.DatosPersonales.models import TeacherPersonalInformation


class Sede(models.Model):
    """Model definition for Sede."""
    name = models.CharField(verbose_name="Nombre", max_length=250, unique=True)
    addr = models.CharField(verbose_name="Dirección", max_length=100, blank=True)
    openhor = models.TimeField(verbose_name="Apertura")
    closehor = models.TimeField(verbose_name="Cierre")

    class Meta:
        """Meta definition for Sede."""
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'

    def __str__(self):
        """Unicode representation of Sede."""
        return "%s" % self.name

    def get_absolute_url(self):
        """Return absolute url for Sede."""
        return reverse('Sede.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):
        '''Admin View for Edition'''    
        list_display = ('name', 'addr', 'openhor', 'closehor')
        search_fields = ('name',)
        ordering = ('name',)


class Edition(models.Model):
    """Model definition for Edition. Jul 2020-Jul 2021"""
    name = models.CharField(max_length=17, verbose_name="Curso - Edición", 
        unique=True, blank=False, 
        default="%s-%s" % (date.today().strftime("%b %Y"), "%s %s" % (date.today().strftime("%b"), date.today().year + 1))
    )
    dateinit = models.DateField(verbose_name="Fecha de Inicio", default=timezone.now)
    dateend = models.DateField(verbose_name="Fecha de Fin", default=date.today() + timedelta(days=180))

    class Meta:
        """Meta definition for Edition."""
        verbose_name = 'Curso - Edición'
        verbose_name_plural = 'Curso - Ediciones'

    def __str__(self):
        """Unicode representation of Edition."""
        return "%s" % self.name

    def get_absolute_url(self):
        """Return absolute url for Edition."""
        return reverse('Edition.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):
        '''Admin View for Edition'''    
        list_display = ('name', 'dateinit', 'dateend')
        search_fields = ('name',)
        ordering = ('name',)


class Area(models.Model):
    name  = models.CharField(max_length=50, verbose_name="Nombre", unique=True)
    description = models.TextField(max_length=1000, verbose_name="Descripcion", blank=True)
    typeOf = models.BooleanField(verbose_name="¿Es docente?", default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Curso - Áreas'

    def get_absolute_url(self):
        return reverse('Area.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):
        '''Admin View for Area'''    
        list_display = ('name', 'description', 'typeOf')
        list_filter = ('typeOf',)
        search_fields = ('name', 'description', 'typeOf')
        ordering = ('name',)
# <> Fin Area


class CourseInformation(models.Model):
    """Model definition for Curso."""
    area = models.ForeignKey("Area", verbose_name="Area", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    image = models.FileField(upload_to=os.path.join('static', 'image', 'perfil', 'course'),
                             default=os.path.join('static', 'image', 'perfil', 'course', 'perfildefault.jpg'), 
                             null=True, blank=True)
    capacity = models.PositiveSmallIntegerField(default=12, verbose_name="Capacidad")
    openregistre = models.DateField(blank=True, verbose_name="Inicio Admisión")
    deadline = models.DateField(blank=True, verbose_name="Fin Admisión")
    description = models.TextField(max_length=5000, blank=True, verbose_name="Descripión")
    
    price = models.PositiveSmallIntegerField(default=20, verbose_name="Precio")
    curriculum = models.TextField(max_length=5000, blank=True, verbose_name="Curriculum")
    requirements = models.TextField(max_length=5000, blank=True, verbose_name="Requisitos")
    
    haveApplication = models.BooleanField(default=False, verbose_name="¿Tiene Formulario de Aplicación?") 

    yearMin = models.PositiveSmallIntegerField(default=18, verbose_name="Edad Minima")
    yearMax = models.PositiveSmallIntegerField(default=40, verbose_name="Edad Máxima")
    
    isService = models.BooleanField(default=False, verbose_name="¿Es un servicio?")

    groups = []    
    subjects = []

    adminteachers = models.ManyToManyField(TeacherPersonalInformation, related_name="teachers", related_query_name="teacher_admin", verbose_name="Profesores Encargados")
    sedes = models.ManyToManyField(Sede, related_name="sedes", related_query_name="sedes", verbose_name="Sede(s)")

    programa = models.FileField(
        verbose_name="Programa", 
        upload_to=os.path.join('static', 'cursos', 'programas'), 
        blank=True, 
        null=True
    )

    reglamento = models.FileField(
        verbose_name="Reglamento", 
        upload_to=os.path.join('static', 'cursos', 'programas'), 
        blank=True, 
        null=True
    )

    class Meta:
        """Meta definition for Curso."""
        verbose_name = 'Curso / Servicio'
        verbose_name_plural = 'Curso - Cursos y Servicios'

    def __str__(self):
        """Unicode representation of Curso."""
        return "%s - %s" % (self.name, self.area)

    def get_absolute_url(self):
        """Return absolute url for Curso."""
        return reverse('CourseInformation.views.details', args=[str(self.id)])

    def getHaveApplication(self):
        return self.haveApplication

    class Admin(ModelAdmin):
        fields = ["name", "area", "isService", "image", "capacity", "openregistre", "deadline", 
                  "description", "yearMin", "yearMax", "haveApplication", 
                  "price", "curriculum", "requirements", "adminteachers", "sedes", "programa", "reglamento"]
        ordering = ["area", "name", "capacity", "openregistre"]
        search_fields = ["name", "openregistre"]
        list_filter = ["sedes", "area", "isService", "haveApplication"]
        list_display = ["name", "area", "isService", "capacity", "haveApplication", "openregistre", "deadline"]
