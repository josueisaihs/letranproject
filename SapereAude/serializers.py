from rest_framework import serializers
from . import models


class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Edition
        fields = ['slug', 'name', 'datepub', 'dateupdate']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = ['slug', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ['slug', 'name', 'lastname', 'grade', 'filial']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['slug', 'authors', 'title', 'abstract', 'subtitle', 'section', 'datepub', 'dateupdate',
        'image', 'datepub', 'dateupdate']