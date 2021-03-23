from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.timezone import now
from django.utils.text import slugify

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

@admin.register(Suscriptor)
class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip', 'fecha')
    search_fields = ('email',)
    ordering = ('-fecha', 'email',)
    readonly_fields = ('fecha',)

class Release(models.Model):
    """Model definition for Release."""
    title = models.CharField(max_length=100, verbose_name="Título")
    resume = models.TextField(verbose_name="Resumen", max_length=150, default="", null=True)
    background = ImageField(upload_to=os.path.join('static', 'image', 'release'), null=True, blank=True, verbose_name="Imagen Fondo")
    slug = models.SlugField(max_length=140, unique=True)
    body = CKEditor5Field('Cuerpo', config_name='default', default="<p>Sin texto</p>")
    date = models.DateTimeField(verbose_name="Fecha de Publicación")
    publicar = models.BooleanField(verbose_name="¿Publicar?", default=False)

    class Meta:
        """Meta definition for Release."""
        unique_together = [('title', 'slug')]
        verbose_name = 'Comunicado'
        verbose_name_plural = 'Index - Comunicados'

    def bodysend(self, m=100):
        return self.body[:m].replace("<p>", "").replace("</p>", "\n")
    
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Release.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Release."""
        return "%s" % self.title
    
@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    '''Admin View for Release'''
    list_display = ('title', 'date', 'slug', 'publicar', 'background')
    readonly_fields = ('slug',)
    list_filter = ('publicar',)
    search_fields = ('title',)
    ordering = ('-date',)


class News(models.Model):
    category = models.CharField(max_length=100, verbose_name="Categría", choices=(
        ("Iglesia", "Iglesia"),
        ("Orden Predicadores", "Orden Predicadores"),
        ("Vicariato 'Pedro de Córdoba'", "Vicariato 'Pedro de Córdoba'"),
        ("Educación", "Educación"),
        ("Nacionales", "Nacionales"),
        ("Mundo", "Mundo"),
        ("Tecnología", "Tecnología"),
        ("CFBC", "CFBC")
    ), default="Iglesia")
    resume = models.TextField(verbose_name="Resumen", max_length=250, default="")
    title = models.CharField(max_length=100, verbose_name="Título")
    slug = models.SlugField(max_length=140, default="")
    body = CKEditor5Field('Cuerpo', config_name='extends', default="<p>Sin texto</p>")
    link = models.URLField(verbose_name="Enlace", blank=True)
    image = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Principal")
    date = models.DateTimeField(verbose_name="Fecha de Publicación")

    image_1 = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Galería 1")
    image_2 = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Galería 2")
    image_3 = ImageField(upload_to=os.path.join('static', 'image', 'news'), null=True, blank=True, verbose_name="Imagen Galería 3")

    class Meta:
        unique_together = [('title', 'slug')]
        verbose_name = 'Index - Noticia'
        verbose_name_plural = 'Index - Noticias'

    def __str__(self):
        """Unicode representation of Noticias."""
        return "%s" % self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while News.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Noticias."""
        return reverse('News.views.details', args=[str(self.id)])
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ('category', 'title', 'link', 'date', 'image', 'resume', 'body', 'slug')
    list_display = ('category', 'title', 'link', 'date',)
    search_fields = ('title',)
    ordering = ('-date', 'title')
    list_filter = ('category',)
    readonly_fields = ('slug',)


class EventsDate(models.Model):
    dateEnv = models.DateTimeField(verbose_name="Fecha Inicio")
    dateFin = models.DateTimeField(verbose_name="Fecha Fin", default=now)
    
    class Meta:
        unique_together = [('dateEnv', 'dateFin')]
        verbose_name = 'Index - Evento Fecha'
        verbose_name_plural = 'Index - Eventos Fechas'

    def __str__(self):
        return "%s - %s" % (self.dateEnv, self.dateFin)

@admin.register(EventsDate)
class EventsDateAdmin(admin.ModelAdmin):
    list_display = ('dateEnv', 'dateFin')
    search_fields = ('dateEnv', 'dateFin')
    ordering = ('-dateEnv',)

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
    
@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    fields = ('user', 'name', 'date', 'place', 'image', 'file', 'dateEnvs', 'body', 'google_maps')
    list_display = ('name', 'date', 'place', 'image', 'file')
    search_fields = ('name', 'place')
    ordering = ('-date', 'name', 'place')


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

@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
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

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
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

@admin.register(HeaderIndex)
class HeaderIndexAdmin(admin.ModelAdmin):
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

@admin.register(SectionSuscribete)
class SectionSuscribeteAdmin(admin.ModelAdmin):
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

@admin.register(SectionComments)
class SectionCommentsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class Recurso(models.Model):
    slug = models.SlugField(max_length=140, default="")
    name = models.CharField(max_length=50, verbose_name="Nombre", unique=True)
    recurso = models.FileField(verbose_name="Recurso", 
    upload_to='static/recurso/%Y/%m/%d/%H/%M/', null=True, blank=True)
    image = ImageField(upload_to=os.path.join('static', 'recurso', 'miniatura'), null=True, blank=True)
    tipo = models.CharField(max_length=20, verbose_name="Tipo", 
        choices=(
                ("imagen", "Imagen"), ("documento", "Documento"), ("video", "Video"), ("audio", "Audio"),
                ("conferencia", "Conferencia"), ("programa", "Programa"), ("reglamento", "Reglamento"),
                ("html", "HTML"), ("css", "CSS"), ("js", "JavaScript"), ("python", "Python")
            )
    )
    uploaddate = models.DateField(verbose_name="Fecha", auto_now=True, blank=False, 
        editable=False)
    access = models.BooleanField(verbose_name="Acceso Público", default=False, 
    help_text="Si mantiene sin marcar solo podrá ser descargado por los usuarios a los que le comparta el link")

    courses = models.ManyToManyField("Docencia.CourseInformation", verbose_name="Asignar Curso", blank=True, 
    help_text="Si agrega curso(s) este recurso será visible para los estudiantes, en caso de NO haber marcado Acceso Público.")
    
    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Index - Recursos'

    def __str__(self):
        return "%s" % self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Recurso.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
            self.name = self.slug
        super().save(*args, **kwargs)

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):    
    list_display = ('name', 'tipo')
    list_filter = ('tipo', 'access')
    readonly_fields = ('uploaddate', 'slug')
    search_fields = ('name', 'tipo', 'courses__name')
    ordering = ('-uploaddate',)


class RedesSociales(models.Model):
    """Model definition for RedesSociales."""
    consumer_key = models.CharField(verbose_name="Twitter > Consumer Key", max_length=100)
    consumer_secret = models.CharField(verbose_name="Twitter > Consumer Secret", max_length=100)
    access_token = models.CharField(verbose_name="Twitter > Access Token", max_length=100)
    access_token_secret = models.CharField(verbose_name="Twitter > Access Token Secret", max_length=100)
    facebook_token = models.CharField(verbose_name="Facebook > Token", max_length=250, blank=True, null=True)
    facebook_id = models.CharField(verbose_name="Facebook > ID", max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)

    class Meta:
        """Meta definition for RedesSociales."""
        unique_together = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret', 'facebook_token', 'facebook_id']
        verbose_name = 'Redes Sociales Tokens'
        verbose_name_plural = 'Index - Redes Sociales Tokens'

    def __str__(self):
        """Unicode representation of RedesSociales."""
        return "%s" % self.consumer_key

@admin.register(RedesSociales)
class RedesSocialesAdmin(admin.ModelAdmin):    
    list_display = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret', 'facebook_token', 'facebook_id')
    search_fields = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret', 'facebook_token', 'facebook_id')

    

    


