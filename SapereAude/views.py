import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from . import models
from . import serializers
from django.db.models import Q

TEMPLETE_PATH = "sapereaude/%s.html"


def index(req, edition=""):
    if (edition == ""):
        edition = models.Edition.objects.all().order_by('-datepub').first()
        return redirect('/sapereaude/%s' % edition.slug)
    else:
        edition = models.Edition.objects.get(slug=edition)

    editions = models.Edition.objects.all()
    return render(req, TEMPLETE_PATH % 'index', locals())

def article(req, edition, article):
    edition = models.Edition.objects.get(slug=edition)
    article = models.Article.objects.get(slug=article)

    editions = models.Edition.objects.all()
    return render(req, TEMPLETE_PATH % 'article', locals())

def section(req, edition, section):
    edition = models.Edition.objects.get(slug=edition)
    section = models.Section.objects.get(slug=section)

    editions = models.Edition.objects.all()
    return render(req, TEMPLETE_PATH % 'section', locals())

class Edition(View):
    def get(self, request, *args, **kwargs):
        editions = serializers.EditionSerializer(models.Edition.objects.all(), many=True)
        return JsonResponse(editions.data, safe=False)

    def post(self, request, *args, **kwargs):
        post_data = json.loads(request.body.decode('utf-8'))
        editions = serializers.EditionSerializer(models.Edition.objects.filter(slug=post_data['edition']), many=True)
        return JsonResponse(editions.data, safe=False)

class Section(View):
    def get(self, request, edition, *args, **kwargs):
        sections = serializers.SectionSerializer(models.Section.objects.filter(edition=models.Edition.objects.get(slug=edition)), many=True)
        return JsonResponse(sections.data, safe=False)

    def post(self, request, *args, **kwargs):
        post_data = json.loads(request.body.decode('utf-8'))
        section = serializers.SectionSerializer(models.Section.objects.filter(pk=post_data['section']), many=True)
        return JsonResponse(section.data, safe=False)

class Author(View):
    def get(self, request, *args, **kwargs):
        authors = serializers.AuthorSerializer(models.Author.objects.all(), many=True)
        return JsonResponse(authors.data, safe=False)

    def post(self, request, *args, **kwargs):
        post_data = json.loads(request.body.decode('utf-8'))
        authors = serializers.AuthorSerializer(models.Author.objects.filter(pk__in=post_data['authors']), many=True)
        return JsonResponse(authors.data, safe=False)

class ArticleRandom(View):
    def get(self, request, *args, **kwargs):
        article = serializers.ArticleSerializer(models.Article.objects.all(), many=True)
        return JsonResponse(article.data, safe=False)