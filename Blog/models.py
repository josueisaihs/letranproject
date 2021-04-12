import os

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.utils.timezone import now
from django.contrib.auth.models import User, Group

class Author(models.Model):
    """Model definition for Author."""
    slug = models.SlugField(max_length=250, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(_("Nombre"), max_length=50)
    lastname = models.CharField(_("Apellido"), max_length=50)
    grade = models.CharField('Grado Científico', max_length=20,
        choices=(("Ing.", "Ingeniero"), ("Arq.", "Arquitecto"), ("Lic.", "Licenciado"), ("Ms.C.", "Master en Ciencias"),
                ("Dr.C.", "Doctor en Ciencias"), ("PhD.C.", "Postdoctor en Ciencias"), ("", "Ninguno")), default=""
    )
    
    ocupation = models.CharField(_("Ocupacion"), max_length=150)
    resume = models.TextField(_("Resumé"))
    photo = models.ImageField(_("Foto"), upload_to=os.path.join('static', 'blog', 'author'))

    class Meta:
        """Meta definition for Author."""
        unique_together = [("name", "lastname")]
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def getFullname(self):
        return "%s %s" % (self.name, self.lastname)

    def __str__(self):
        """Unicode representation of Author."""
        return self.getFullname()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def _get_unique_slug(self):
        slug = slugify(self.getFullname())
        unique_slug = slug
        num = 1
        while Author.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    '''Admin View for Author'''
    list_display = ('user', 'name', 'lastname', 'grade')
    readonly_fields = ('slug',)
    search_fields = ('name', 'lastname')
    ordering = ('lastname', 'name')

class Blog(models.Model):
    """Model definition for Blog."""
    slug = models.SlugField(max_length=250, default="")
    name = models.CharField(_("Nombre"), max_length=150, unique=True)
    description = CKEditor5Field('Descripción', config_name='extends')
    authors = models.ManyToManyField("Blog.Author", verbose_name=_("Autor(es)"))
    image = models.ImageField(_("Imagen"), upload_to=os.path.join('static', 'blog', 'blog'))
    active =  models.BooleanField(_("Activo"), default=False)

    class Meta:
        """Meta definition for Blog."""
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        """Unicode representation of Blog."""
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Author.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''
    list_display = ('name', 'active')
    readonly_fields = ('slug',)
    search_fields = ('name', 'name__authors__name', 'name__authors__lastname')
    ordering = ('name',)

class Article(models.Model):
    slug = models.SlugField('Slug', max_length=250)
    blog = models.ForeignKey("Blog.Blog", verbose_name='Blog', on_delete=models.CASCADE)
    authors = models.ManyToManyField("Blog.Author", verbose_name="Autor(es)")
    title = models.CharField('Título', max_length=250)
    subtitle = models.CharField('Subtítulo', max_length=250, default="", blank=True)
    abstract = models.TextField("Resumen")
    image = models.ImageField('Imagen', upload_to='static/blog/%Y/%m/%d/%H/%M/')
    body = CKEditor5Field('Cuerpo', config_name='extends', default="<p>Sin texto</p>")
    datepub = models.DateField('Publicación', auto_now=True)
    dateupdate = models.DateField('Última Actualización', auto_now=True)

    topost = models.BooleanField(_("Publicar"), default=False)
    allow = models.BooleanField(_("Permitir"), default=False)

    class Meta:
        """Meta definition for MODELNAME."""
        unique_together = [('blog', 'title')]
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
    list_display = ('title', 'subtitle', 'blog', 'datepub', 'dateupdate')
    list_filter = ('blog', 'authors__ocupation', 'allow', 'topost')
    readonly_fields = ('slug',)
    search_fields = ('title', 'subtitle', 'abstract', 'authors__name', 'authors__lastname', 
    'author__grade', 'blog__name', )
    ordering = ('-datepub', '-dateupdate', 'title')
    date_hierarchy = 'datepub'