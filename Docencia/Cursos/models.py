from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.core.validators import MinValueValidator

from easy_thumbnails.fields import ThumbnailerImageField as ImageField

import os
from datetime import date, timedelta
from decimal import Decimal

from Docencia.Plataforma.models import Class
from Docencia.Index.models import Recurso


class Sede(models.Model):
    """Model definition for Sede."""
    name = models.CharField(verbose_name="Nombre", max_length=250, unique=True)
    openhor = models.TimeField(verbose_name="Apertura")
    closehor = models.TimeField(verbose_name="Cierre")
    isprincipal = models.BooleanField(verbose_name="¿Es la Sede Principal?", default=False)
    street = models.CharField(max_length=100, null=True, blank=True, verbose_name="Calle")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Municipio")
    state = models.CharField(max_length=50, null=True, blank=True, verbose_name="Provincia")
    cellphone = models.CharField(max_length=8, blank=True, null=True, verbose_name="Móvil")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    reglamento = models.FileField(
        verbose_name="Reglamento", 
        upload_to=os.path.join('static', 'sedes', 'reglamentos'), 
        blank=True, 
        null=True
    )

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

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    '''Admin View for Edition'''    
    list_display = ('name', 'isprincipal', 'openhor', 'closehor', 'street', 'city', 'state', 'cellphone', 'email', 'reglamento')
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

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
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

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    '''Admin View for Area'''    
    list_display = ('name', 'description', 'typeOf')
    list_filter = ('typeOf',)
    search_fields = ('name', 'description', 'typeOf')
    ordering = ('name',)
# <> Fin Area

class CourseCategory(models.Model):
    """Model definition for Categoria."""

    name = models.CharField(verbose_name="Nombre", unique=True, max_length=100, default="Curso")

    class Meta:
        """Meta definition for Categoria."""

        verbose_name = 'Categoría'
        verbose_name_plural = 'Curso - Categorías'

    def __str__(self):
        """Unicode representation of Categoria."""
        return "%s" % self.name

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)    


class CourseSchedule(models.Model):
    """Model definition for CourseSchedule."""
    weekday = models.CharField(max_length=14, choices=(
        ("Lun.", "Lunes"),
        ("Mar.", "Martes"),
        ("Mié.", "Miércoles"),
        ("Jue.", "Jueves"),
        ("Vie.", "Viernes"),
        ("Sáb.", "Sábado"),
        ("Lun.-Vie.", "Lunes a Viernes"),
        ("Lun.-Sáb.", "Lunes a Sábado"),
        ("Lun.,Mié.,Vie.", "Lunes, Miércoles, Viernes"),
        ("Mar.,Jue.", "Martes, Jueves"),
    ), default="Lun.")
    dateIni = models.TimeField(verbose_name="Fecha Inicio")
    dateFin = models.TimeField(verbose_name="Fecha Fin", default=now)

    class Meta:
        unique_together = [('weekday', 'dateIni', 'dateFin')]
        verbose_name = 'Horario'
        verbose_name_plural = 'Cursos - Horarios'

    def __str__(self):
        return "%s (%s-%s)" % (self.weekday, self.dateIni, self.dateFin)

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('weekday', 'dateIni', 'dateFin')
    search_fields = ('weekday', 'dateIni', 'dateFin')
    ordering = ('dateIni',)


class CourseInformation(models.Model):
    """Model definition for Curso."""
    slug = models.SlugField(max_length=250, default="")
    area = models.ForeignKey("Area", verbose_name="Area", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    image = ImageField(upload_to=os.path.join('image', 'perfil', 'course'), null=True, blank=True)
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
    category = models.ForeignKey("CourseCategory", verbose_name="Categoría", on_delete=models.CASCADE, blank=True, null=True)

    groups = []    
    subjects = []

    adminteachers = models.ManyToManyField('Docencia.TeacherPersonalInformation', related_name="teachers", related_query_name="teacher_admin", verbose_name="Profesores Encargados")
    sedes = models.ManyToManyField(Sede, related_name="sedes", related_query_name="sedes", verbose_name="Sede(s)")

    recursos = []

    comunicate = models.TextField(verbose_name="Comunicado (Solo visible en el CAMPUS VIRTUAL)", blank=True, default='')

    programa = models.FileField(
        verbose_name="Programa", 
        upload_to=os.path.join('media', 'static', 'cursos', 'programas'), 
        blank=True, 
        null=True
    )

    reglamento = models.FileField(
        verbose_name="Reglamento", 
        upload_to=os.path.join('static', 'cursos', 'programas'), 
        blank=True, 
        null=True
    )

    schedules = models.ManyToManyField("CourseSchedule", verbose_name="Horario(s)", blank=True)
    starts = models.SmallIntegerField(verbose_name="Puntuación", default=4)


    minCredict = models.PositiveSmallIntegerField(
        verbose_name="Creditos Minimos (Por semestre)",
        default=6
    )
    duration = models.PositiveSmallIntegerField(verbose_name="Duración (Semestres)", default=2)

    class Meta:
        """Meta definition for Curso."""
        verbose_name = 'Curso / Servicio'
        verbose_name_plural = 'Curso - Cursos y Servicios'
    
    def getSubjects(self):
        return SubjectInformation.objects.filter(course=self.pk)

    def getGroups(self):
        return GroupInformation.objects.filter(course=self.pk)

    def getRecursos(self):
        return Recurso.objects.filter(courses=self.pk)

    def __str__(self):
        """Unicode representation of Curso."""
        return "%s - %s" % (self.name, self.area)

    def get_absolute_url(self):
        """Return absolute url for Curso."""
        return reverse('CourseInformation.views.details', args=[str(self.id)])

    def getHaveApplication(self):
        return self.haveApplication

    def isAvailableRegistre(self):
        return self.openregistre <= date.today() <= self.deadline

    def _get_unique_slug(self):
        slug = slugify("%s %s" % (self.area.name, self.name))
        unique_slug = slug
        num = 1
        while CourseInformation.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(CourseInformation)
class CourseInformationAdmin(admin.ModelAdmin):
    fields = ["name", "area", "isService", "category", "image", "capacity", "openregistre", "deadline", 
                "description", "yearMin", "yearMax", "haveApplication", 
                "price", "curriculum", "requirements", "adminteachers", "sedes", "programa", 
                "reglamento", "schedules", "starts", "slug", "minCredict", "duration", 'comunicate']
    ordering = ["area", "name", "capacity", "openregistre"]
    search_fields = ["name", "openregistre", "area__name", "sedes__name", "category__name"]
    readonly_fields = ('slug',)
    list_filter = ["sedes", "area", "category", "isService", "haveApplication"]
    list_display = ["name", "area", "category", "isService", "capacity", "haveApplication", "openregistre", "deadline"]

class GroupInformation(models.Model):
    """Model definition for GroupInformation."""
    slug = models.SlugField('Slug', default="", max_length=200)
    name = models.CharField(verbose_name="Nombre", max_length=150)
    edition = models.ForeignKey(Edition, verbose_name="Edición", on_delete=models.CASCADE)
    course = models.ForeignKey(CourseInformation, verbose_name="Curso", on_delete=models.CASCADE)
    teachers = models.ManyToManyField('Docencia.TeacherPersonalInformation', verbose_name="Profesor(s)")
    students = models.ManyToManyField('Docencia.StudentPersonalInformation', verbose_name="Estudiante(s)", blank=True)

    class Meta:
        """Meta definition for GroupInformation."""
        unique_together = [('name', 'edition', 'course')]
        verbose_name = 'Grupo'
        verbose_name_plural = 'Cursos - Grupos'

    def _get_unique_slug(self):
        slug = slugify("%s %s %s" % (self.course.area.name, self.course.name, self.name))
        unique_slug = slug
        num = 1
        while GroupInformation.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of GroupInformation."""
        return "%s-%s %s" % (self.course, self.edition, self.name)

@admin.register(GroupInformation)
class GroupInformationAdmin(admin.ModelAdmin):
    '''Admin View for GroupInformation'''
    list_display = ('name', 'edition', 'course')
    list_filter = ('edition', 'course', 'course__area')
    search_fields = ('name', 'edition__name', 'course__name', 'course__area__name', 'teachers__name', 'teachers__lastname',
    'students__name', 'students__lastname')
    ordering = ('name',)
    readonly_fields = ["slug",]

class SubjectInformation(models.Model):
    # Asignatura
    slug = models.SlugField(max_length=250, default="")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    course = models.ForeignKey(CourseInformation, verbose_name="Curso", on_delete=models.CASCADE)
    credicts = models.DecimalField(verbose_name="Creditos", max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    showCredicts = models.BooleanField(default=False, verbose_name="Mostrar Creditos")
    active = models.BooleanField(default=True, verbose_name="Activada")
    mode = models.CharField(
        verbose_name="Modo",
        max_length=14,
        choices=(
            ("Troncal", "Troncal"),
            ("Obligatoria", "Obligatoria"), 
            ("Optativa", "Optativas"),
            ("Libre Elección", "Libre Elección") 
        ), default="Obligatioria"
    )
    # Certificacion de notas de la asginatura
    needBallot = models.BooleanField(default=False, verbose_name="Boleta de Fin de Estudios")
    teachers = models.ManyToManyField("Docencia.TeacherPersonalInformation", verbose_name="Profesor(es)")
    # TODO la boleta final en base a 10 
    
    description = CKEditor5Field('Descripción', config_name='extends')
    
    evaluations = []
    classes = []
    
    def __str__(self):
        return "%s (%s)" % (self.name, self.course)

    def getClasses(self):
        return Class.objects.filter(subject=self.pk)

    class Meta:
        unique_together= ('name', 'course')
        verbose_name = 'Curso - Asignatura'
        verbose_name_plural = 'Curso - Asignaturas'

    def _get_unique_slug(self):
        slug = slugify("%s %s %s" % (self.course.area.name, self.course.name, self.name))
        unique_slug = slug
        num = 1
        while CourseInformation.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
        
@admin.register(SubjectInformation)
class SubjectInformationAdmin(admin.ModelAdmin):
    fields = ["name", "teachers", "course", "description", "credicts", "showCredicts", 
    "needBallot", "slug", "active", "mode"]
    ordering = ["name", "course", "credicts"]
    search_fields = ["name", "course__name", "course__area__name"]
    list_filter = ["showCredicts", "active", "mode", "needBallot", "course__area"]
    list_display = ["name", "course", "credicts", "showCredicts", "needBallot"]
    readonly_fields = ["slug",]
# <> fin SubjectInformation