from django.db import models
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.timezone import now

from easy_thumbnails.fields import ThumbnailerImageField as ImageField

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
    image = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Principal")

    date = models.DateTimeField(verbose_name="Fecha de Publicación")

    image_1 = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Galería 1")
    image_2 = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Galería 2")
    image_3 = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Galería 3")

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
        fields = ('title', 'link', 'date', 'image', 'image_1', 'image_2', 'image_3', 'body')
        list_display = ('title', 'link', 'date',)
        search_fields = ('title',)
        ordering = ('title', '-date')

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    body = models.TextField(verbose_name="Cuerpo")
    link = models.URLField(verbose_name="Enlace", blank=True)
    autor = models.CharField(max_length=200)
    image = ImageField(upload_to=os.path.join('static', 'image', 'blog'), null=True, blank=True)

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
        list_display = ('title', 'autor', 'link', 'date', 'image')
        search_fields = ('title',)
        ordering = ('title',)

class EventsDate(models.Model):
    dateEnv = models.DateTimeField(verbose_name="Fecha Inicio")
    dateFin = models.DateTimeField(verbose_name="Fecha Fin", default=now)

    class Meta:
        unique_together = [('dateEnv', 'dateFin')]
        verbose_name = 'Index - Evento Fecha'
        verbose_name_plural = 'Index - Eventos Fechas'

    def __str__(self):
        return "%s - %s" % (self.dateEnv, self.dateFin)

    class Admin(ModelAdmin):
        list_display = ('dateEnv', 'dateFin')
        search_fields = ('dateEnv', 'dateFin')
        ordering = ('dateEnv',)

class Events(models.Model):
    """Model definition for Events."""
    name = models.CharField(verbose_name="Nombre", max_length=100)
    body = models.TextField(verbose_name="Descripción", max_length=1000)
    date = models.DateTimeField(verbose_name="Fecha Publicación")
    dateEnvs = models.ManyToManyField("EventsDate", verbose_name="Fecha(s)")
    place = models.CharField(verbose_name="Lugar", max_length=500)
    image = ImageField(upload_to=os.path.join('static', 'event', 'image'), null=True, blank=True)
    file = models.FileField(upload_to=os.path.join('static', 'event', 'file'), null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario", default=1, limit_choices_to={'is_staff': True})
    google_maps = models.TextField(max_length=1000, verbose_name="Embeber Google Maps", blank=True)

    #TODO Añadir suscribirse al evento

    class Meta:
        """Meta definition for Events."""
        unique_together = [("name", "date")]
        verbose_name = 'Evento'
        verbose_name_plural = 'Index - Eventos'

    def __str__(self):
        """Unicode representation of Events."""
        return "%s - %s" % (self.name, self.date)

    def get_absolute_url(self):
        """Return absolute url for Events."""
        return reverse('Events.views.details', args=[str(self.id)])
    
    class Admin(ModelAdmin):
        fields = ('user', 'name', 'date', 'place', 'image', 'file', 'dateEnvs', 'body', 'google_maps')
        list_display = ('name', 'date', 'place', 'image', 'file')
        search_fields = ('name', 'place')
        ordering = ('date',)


class Links(models.Model):
    """Model definition for Links."""
    name = models.CharField(max_length=50, verbose_name="Nombre", unique=True)
    section = models.CharField(verbose_name="Sección", max_length=3, choices=(("enl", "Enlaces Útiles"), ("opr", "Orden Predicadores")), default="enl")
    link = models.URLField(verbose_name="Enlace")

    class Meta:
        """Meta definition for Links."""
        verbose_name = 'Index - Link'
        verbose_name_plural = 'Index - Links'

    def __str__(self):
        """Unicode representation of Links."""
        return "%s" % self.name

    def get_absolute_url(self):
        """Return absolute url for Links."""
        return reverse('Links.views.details', args=[srt(self.id)])

    class Admin(ModelAdmin):
        list_display = ('name', 'link')
        search_fields = ('name',)


class Comments(models.Model):
    """Model definition for Comments."""

    author = models.CharField(max_length=100, verbose_name="Autor", unique=True)
    image = ImageField(upload_to=os.path.join('static', 'image', 'comment'), null=True, blank=True, verbose_name="Foto Perfil")
    body = models.TextField(max_length=1000, verbose_name="Comentario")

    class Meta:
        """Meta definition for Comments."""
        verbose_name = 'Index - Comentario'
        verbose_name_plural = 'Index - Comentario'

    def __str__(self):
        """Unicode representation of Comments."""
        return "%s" % self.author

    def get_absolute_url(self):
        """Return absolute url for Comments."""
        return reverse('Comments.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):
        list_display = ('author', 'body', 'image')
        search_fields = ('author',)

class HeaderIndex(models.Model):
    """Model definition for HeaderIndex."""
    name = models.CharField(max_length=50, verbose_name="Nombre", unique=True)
    background = ImageField(upload_to=os.path.join('static', 'image', 'index', 'bg'), null=True, blank=True, verbose_name="Background Image")
    icon = ImageField(upload_to=os.path.join('static', 'image', 'index', 'icon'), null=True, blank=True, verbose_name="Icon")
    titleLine1 = models.CharField(max_length=20, verbose_name="Título Línea 1")
    titleLine2 = models.CharField(max_length=20, verbose_name="Título Línea 2", blank=True)
    titleLine3 = models.CharField(max_length=20, verbose_name="Título Línea 3", blank=True)
    subtitle = models.CharField(max_length=32, verbose_name="Subtítulo", blank=True)
    
    hadBtn1 = models.BooleanField(verbose_name="Añadir Botón 1", default=False)
    btn1 = models.CharField(verbose_name="Botón 1 Texto", max_length=10, blank=True)
    linkBtn1 = models.CharField(verbose_name="Botón 1 Enlace", blank=True, max_length=25)
    
    hadBtn2 = models.BooleanField(verbose_name="Añadir Botón 2", default=False)
    btn2 = models.CharField(verbose_name="Botón 2 Texto", max_length=10, blank=True)
    linkBtn2 = models.CharField(verbose_name="Botón 2 Enlace", blank=True, max_length=25)

    isVisible = models.BooleanField(default=False, verbose_name="Visible")

    class Meta:
        """Meta definition for ImgenHeaderIndex."""
        verbose_name = 'Index - Header'
        verbose_name_plural = 'Index - Header'

    def __str__(self):
        """Unicode representation of ImgenHeaderIndex."""
        return "%s" % self.name

    def get_absolute_url(self):
        """Return absolute url for SectionSuscribete."""
        return reverse('HeaderIndex.views.details' % self.id)

    class Admin(ModelAdmin):
        fields = ["name", "background", "icon", "titleLine1", "titleLine2", "titleLine3", "subtitle",
                  "hadBtn1", "btn1", "linkBtn1", "hadBtn2", "btn2", "linkBtn2", "isVisible"]
        list_display = ('name',)
        search_fields = ('name',)


class SectionSuscribete(models.Model):
    """Model definition for SectionSuscribete."""
    name = models.CharField(max_length=20, verbose_name="Sección Suscribete")
    students = models.PositiveSmallIntegerField(default=0, verbose_name="Cantidad de Estudiantes [mil]")
    graduados = models.PositiveIntegerField(default=0, verbose_name="Cantidad de Graduados [mil]")
    cursos = models.PositiveIntegerField(default=0, verbose_name="Cantidad Cursos")
    background = ImageField(upload_to=os.path.join('static', 'image', 'index', 'bg'), null=True, blank=True, verbose_name="Background Image")

    class Meta:
        """Meta definition for SectionSuscribete."""

        verbose_name = 'Index - Sección Suscríbete'
        verbose_name_plural = 'Index - Sección Suscríbete'

    def __str__(self):
        """Unicode representation of SectionSuscribete."""
        return "%s" % self.name

    def get_absolute_url(self):
        """Return absolute url for SectionSuscribete."""
        return reverse('SectionSuscribete.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):
        list_display = ('name', 'background', 'students', 'graduados', 'cursos')
        search_fields = ('name',)

class SectionComments(models.Model):
    """Model definition for SectionComments."""
    name = models.CharField(max_length=20, verbose_name="Nombre", unique=True)
    background = ImageField(upload_to=os.path.join('static', 'image', 'index', 'bg'), null=True, blank=True, verbose_name="Background Image")       

    class Meta:
        """Meta definition for SectionComments."""
        verbose_name = 'Index - Sección Comentario'
        verbose_name_plural = 'Index - Sección Comentarios'

    def __str__(self):
        """Unicode representation of SectionComments."""
        return "%s" % self.name

    def get_absolute_url(self):
        """Return absolute url for SectionComments."""
        return reverse('SectionComments.views.details', args=[str(self.id)])

    class Admin(ModelAdmin):
        list_display = ('name',)
        search_fields = ('name',)

class Recurso(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    recurso = models.FileField(verbose_name="Recurso", 
    upload_to=os.path.join('static', 'recurso'), null=True, blank=True,)
    tipo = models.CharField(max_length=20, verbose_name="Tipo", 
    choices=(
        ("imagen", "Imagen"), 
        ("documento", "Documento"),
        ("video", "Video"),
        )
    )
    uploaddate = models.DateField(verbose_name="Fecha", auto_now=True, blank=False, 
        editable=False)
    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Index - Recursos'

    def __str__(self):
        return "%s" % self.name

    class Admin(ModelAdmin):    
        list_display = ('name', 'tipo')
        list_filter = ('tipo',)
        readonly_fields = ('uploaddate',)
        search_fields = ('name', 'tipo')
        ordering = ('-uploaddate',)


class RedesSociales(models.Model):
    """Model definition for RedesSociales."""

    consumer_key = models.CharField(verbose_name="Twitter > Consumer Key", max_length=100)
    consumer_secret = models.CharField(verbose_name="Twitter > Consumer Secret", max_length=100)
    access_token = models.CharField(verbose_name="Twitter > Access Token", max_length=100)
    access_token_secret = models.CharField(verbose_name="Twitter > Access Token Secret", max_length=100)
    active = models.BooleanField(default=False)

    class Meta:
        """Meta definition for RedesSociales."""
        unique_together = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']
        verbose_name = 'Redes Sociales Tokens'
        verbose_name_plural = 'Index - Redes Sociales Tokens'

    def __str__(self):
        """Unicode representation of RedesSociales."""
        return "%s" % self.consumer_key

    class Admin(ModelAdmin):    
        list_display = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')
        search_fields = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')

    

    


