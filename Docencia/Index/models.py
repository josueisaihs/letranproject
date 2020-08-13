from django.db import models
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import os

class Suscriptor(models.Model):
    """Model definition for Suscriptor."""

    email = models.EmailField(verbose_name="Email", unique=True)
    ip = models.GenericIPAddressField(verbose_name="Dirección IP")
    fecha = models.DateTimeField(auto_now=True, verbose_name="Fecha")

    class Meta:
        """Meta definition for Subscriptor."""
        verbose_name = 'Index - Subscriptor'
        verbose_name_plural = 'Index - Subscriptores'

    def __str__(self):
        """Unicode representation of Subscriptor."""
        return "%s" % (self.email)

    def get_absolute_url(self):
        """Return absolute url for Subscriptor."""
        return reverse('Suscriptor.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):   
        list_display = ('email', 'ip', 'fecha')
        search_fields = ('email',)
        ordering = ('email',)
        readonly_fields = ('fecha',)


class News(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    body = models.TextField(verbose_name="Cuerpo")
    link = models.URLField(verbose_name="Enlace", blank=True)
    image = models.FileField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True)

    date = models.DateTimeField(verbose_name="Fecha de Publicación")

    class Meta:
        verbose_name = 'Index - Noticia'
        verbose_name_plural = 'Index - Noticias'

    def __str__(self):
        """Unicode representation of Noticias."""
        return "%s" % self.title

    def get_absolute_url(self):
        """Return absolute url for Noticias."""
        return reverse('News.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):   
        list_display = ('title', 'body', 'link', 'date', 'image')
        search_fields = ('title',)
        ordering = ('title',)


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    body = models.TextField(verbose_name="Cuerpo")
    link = models.URLField(verbose_name="Enlace", blank=True)
    autor = models.CharField(max_length=200)
    image = models.FileField(upload_to=os.path.join('static', 'image', 'blog'), null=True, blank=True)

    date = models.DateTimeField(verbose_name="Fecha de Publicación")

    class Meta:
        verbose_name = 'Index - Blog Post'
        verbose_name_plural = 'Index - Blog Posts'

    def __str__(self):
        """Unicode representation of Noticias."""
        return "%s" % self.title

    def get_absolute_url(self):
        """Return absolute url for Noticias."""
        return reverse('Post.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):   
        list_display = ('title', 'autor', 'body', 'link', 'date', 'image')
        search_fields = ('title',)
        ordering = ('title',)


class Events(models.Model):
    """Model definition for Events."""
    name = models.CharField(verbose_name="Nombre", max_length=100)
    body = models.TextField(verbose_name="Descripción", max_length=1000)
    date = models.DateTimeField(verbose_name="Fecha Publicación")
    dateEnv = models.DateTimeField(verbose_name="Fecha Evento")
    place = models.CharField(verbose_name="Lugar", max_length=500)

    class Meta:
        """Meta definition for Events."""
        unique_together = [("name", "dateEnv")]
        verbose_name = 'Index - Evento'
        verbose_name_plural = 'Index - Eventos'

    def __str__(self):
        """Unicode representation of Events."""
        return "%s - %s" % (self.name, self.dateEnv)

    def get_absolute_url(self):
        """Return absolute url for Events."""
        return reverse('Events.views.details', args=[str(self.id)])
    
    class Admin(ModelAdmin):
        list_display = ('name', 'body', 'date', 'dateEnv', 'place')
        search_fields = ('name', 'place')
        ordering = ('dateEnv',)
