from django.db import models
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

import os
from datetime import date, timedelta


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
    name = models.CharField(max_length=50, unique=True)
    image = models.FileField(upload_to=os.path.join('static', 'image', 'perfil', 'course'),
                             default=os.path.join('static', 'image', 'perfil', 'course', 'perfildefault.jpg'), 
                             null=True, blank=True)
    capacity = models.PositiveSmallIntegerField(default=12)
    openregistre = models.DateField(blank=True)
    deadline = models.DateField(blank=True)
    description = models.TextField(max_length=1500, blank=True)
    
    price = models.PositiveSmallIntegerField(default=20)
    curriculum = models.TextField(max_length=2000, blank=True)
    requirements = models.TextField(max_length=1000, blank=True)
    
    haveApplication = models.BooleanField(default=False) 

    yearMin = models.PositiveSmallIntegerField(default=18)
    yearMax = models.PositiveSmallIntegerField(default=40)
    
    isService = models.BooleanField(default=False, verbose_name="¿Es un servicio?")

    groups = []    
    subjects = []

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
                  "price", "curriculum", "requirements"]
        ordering = ["area", "name", "capacity", "openregistre"]
        search_fields = ["name", "openregistre"]
        list_filter = ["area", "isService", "haveApplication"]
        list_display = ["name", "area", "isService", "capacity", "haveApplication", "openregistre", "deadline"]
