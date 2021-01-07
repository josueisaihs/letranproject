import os

from django.db import models
from django.utils.text import slugify
from django.contrib import admin
from django.utils.timezone import now

from django_ckeditor_5.fields import CKEditor5Field


class Edition(models.Model):
    slug = models.SlugField("Slug")
    name = models.CharField("Edición", max_length=50)
    datepub = models.DateField("Fecha Publicación", auto_now=True)
    dateupdate = models.DateField("Última Actualización", auto_now=True)
    
    prologuetitle = models.CharField('Prólogo Título', max_length=250, default="")
    prologue = CKEditor5Field('Prólogo Cuerpo', config_name='extends', default="<p>Sin texto</p>")
    author = models.ForeignKey("SapereAude.Author", verbose_name="Autor Prólogo", on_delete=models.CASCADE, blank=True, default=1)

    class Meta:
        unique_together = ('name', 'datepub')
        verbose_name = 'Edition'
        verbose_name_plural = 'Editions'

    def getSections(self):
        return Section.objects.filter(edition__pk=self.pk)

    def getArticles(self):
        return Article.objects.filter(section__edition__pk=self.pk)

    def getRandomArticles(self):
        return Article.objects.filter(section__edition__pk=self.pk).order_by('?')

    def __str__(self):
        return "%s" % self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Edition.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        self.dateupdate = now()

        super().save(*args, **kwargs)

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'datepub', 'dateupdate', 'prologuetitle', 'prologue', 'author')
    # readonly_fields = ('datepub', 'slug', 'dateupdate')
    readonly_fields = ('slug',)
    search_fields = ('name',)
    ordering = ('name', '-datepub')


class Section(models.Model):
    # Secciones de la revista  
    edition = models.ForeignKey("SapereAude.Edition", verbose_name='Edición', on_delete=models.CASCADE)
    slug = models.SlugField('Slug')
    name = models.CharField('Nombre', max_length=50)

    class Meta:
        """Meta definition for Divition."""
        unique_together = [('edition', 'name')]
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'

    def __str__(self):
        """Unicode representation of Divition."""
        return "%s" % self.name

    def getArticles(self):
        return Article.objects.filter(section__pk=self.pk)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Section.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'edition', 'slug')
    readonly_fields = ('slug',)
    search_fields = ('edition__name', 'name',)
    ordering = ('name',)

class Author(models.Model):
    slug = models.SlugField('Slug')
    grade = models.CharField('Grado Científico', max_length=20,
        choices=(("Ing.", "Ingeniero"), ("Arq.", "Arquitecto"), ("Lic.", "Licenciado"), ("Ms.C.", "Master en Ciencias"),
                ("Dr.C.", "Doctor en Ciencias"), ("PhD.C.", "Postdoctor en Ciencias"), ("", "Ninguno")), default=""
    )
    name = models.CharField('Nombre', max_length=50)
    lastname = models.CharField('Apellido', max_length=100)
    filial = models.CharField("Filial", max_length=250)

    def fullname(self):
        return "%s %s %s" % (self.grade, self.name, self.lastname)

    class Meta:
        """Meta definition for Author."""
        unique_together = [('name', 'lastname')]
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        """Unicode representation of Author."""
        return "%s %s" % (self.name, self.lastname)

    def _get_unique_slug(self):
        slug = slugify(self.__str__())
        unique_slug = slug
        num = 1
        while Author.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'grade', 'filial')
    list_filter = ('filial', 'grade')
    readonly_fields = ('slug',)
    search_fields = ('name', 'lastname', 'grade')
    ordering = ('name', 'lastname', 'filial')


class Article(models.Model):
    slug = models.SlugField('Slug')
    section = models.ForeignKey("SapereAude.Section", verbose_name='Article', on_delete=models.CASCADE)
    authors = models.ManyToManyField("SapereAude.Author", verbose_name="Autor(es)")
    title = models.CharField('Título', max_length=250)
    subtitle = models.CharField('Subtítulo', max_length=250)
    abstract = models.TextField("Resumen")
    image = models.ImageField('Imagen', upload_to='static/recurso/%Y/%m/%d/%H/%M/')
    body = CKEditor5Field('Cuerpo', config_name='extends', default="<p>Sin texto</p>")
    datepub = models.DateField('Publicación', auto_now=True)
    dateupdate = models.DateField('Publicación', auto_now=True)

    class Meta:
        """Meta definition for MODELNAME."""
        unique_together = [('section', 'title')]
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return '%s' % self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        self.dateupdate = now()
        super().save(*args, **kwargs)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'section', 'datepub', 'dateupdate')
    list_filter = ('section', 'authors__filial')
    readonly_fields = ('slug',)
    search_fields = ('title', 'subtitle', 'abstract', 'authors__name', 'authors__lastname', 
    'author__grade', 'section__name', )
    ordering = ('-datepub', '-dateupdate')

