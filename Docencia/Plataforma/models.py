from django.db import models
# from django_ckeditor_5.fields import CKEditor5Field
from django.contrib import admin
from django.utils.text import slugify

from Docencia.Cursos.models import CourseInformation

class Class(models.Model):
    """Model definition for Class."""
    slug = models.SlugField(max_length=250, default="")
    subject = models.ForeignKey("Docencia.SubjectInformation", verbose_name="Asignatura", 
    on_delete=models.CASCADE, default=1)
    name = models.CharField(verbose_name="Nombre", max_length=100)
    # body=CKEditor5Field('Cuerpo', config_name='extends')
    body = models.TextField()
    uploaddate = models.DateField('Fecha Creación', auto_now=True)
    datepub = models.DateTimeField('Fecha Pub.', auto_now=False, auto_now_add=False)
    resources =  models.ManyToManyField("Docencia.Recurso", verbose_name="Recursos", blank=True, limit_choices_to={'access': False})

    class Meta:
        """Meta definition for Class."""
        unique_together = ('subject', 'name')
        verbose_name = 'Clase'
        verbose_name_plural = 'Plataforma - Clases'

    def __str__(self):
        """Unicode representation of Class."""
        return "%s %s (%s)" % (self.subject, self.name, self.uploaddate)

    def slugConst(self):
        return "%s %s %s %s" % (self.subject.course.area.name, self.subject.course.name, self.subject.name, self.name)
    
    def _get_unique_slug(self):
        slug = slugify(self.slugConst())
        unique_slug = slug
        num = 1
        while Class.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    '''Admin View for Class'''
    list_display = ('subject', 'name', 'uploaddate', 'datepub')
    list_filter = ('subject__course', 'subject__course__area')
    search_fields = ('subject__course__name', 'subject__course__sede__name', 'subject__name', 'subject__course__area__name')
    ordering = ('-uploaddate',)
    readonly_fields = ('uploaddate', 'slug')