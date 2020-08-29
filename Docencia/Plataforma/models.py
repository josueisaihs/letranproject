from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib import admin

class Article(models.Model):
    title=models.CharField('Title', max_length=200)
    text=CKEditor5Field('Text', config_name='extends')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass