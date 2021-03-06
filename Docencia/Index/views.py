from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator

from datetime import datetime

from Docencia.Cursos.models import CourseInformation, Area, Sede, CourseCategory
from Docencia.Index.models import HeaderIndex, News, SectionSuscribete, Suscriptor, SectionComments, Comments, Links, Events, Recurso, Release

from .scrapping import getMetaDatos

TEMPLETE_PATH = "home/%s.html"
cantpaginator = 4

import Docencia.tasks as tasks

# @cache_page(60 * 15)
def index(request):  
    navindex = "active"
    news = News.objects.filter(date__lte=datetime.today()).order_by("-date")[:4]

    events = Events.objects.filter(date__lte=datetime.today()).order_by("-date")[:4]

    suscribete = SectionSuscribete.objects.all().first()

    seccion_coment = SectionComments.objects.all().first()

    comments = Comments.objects.all().order_by("?")[:2]

    comunicados = Release.objects.filter(publicar=True).order_by('-date')[:4]

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)

    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(request, TEMPLETE_PATH % "index", locals())

@require_POST
def previewLink(req):
    url = req.POST.get("q")
    print(url)
    data = getMetaDatos(url)
    print(data)
    return JsonResponse(data)

@require_POST
def suscribeteAjax(req):
    suscriptor = Suscriptor()
    email = req.POST.get('email')
    suscriptor.email = email
    suscriptor.ip = req.META.get('REMOTE_ADDR')

    try:
        suscriptor.save()

        response_data = {
                'Exito': "True"
        }

        tasks.verificar_email(email)
    except:
        response_data = {
            'Exito': "False"
        }
    return JsonResponse(response_data)

# @cache_page(60 * 15)
def eventos(req):
    naveventos = "active"
    paginador = Paginator( 
        Events.objects.filter(date__lte=datetime.today()).order_by('-date'), 
        cantpaginator
    )    
    page_number = req.GET.get('page')
    page_obj = paginador.get_page(page_number)

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "eventos", locals())

# @cache_page(60 * 15)
def evento(req, pk):
    naveventos = "active"
    event = Events.objects.get(pk=pk)
    events = Events.objects.filter(date__lte=datetime.today()).exclude(pk=pk).order_by('-date')[:6]
    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "evento", locals())

# @cache_page(60 * 15)
def cursos(req):
    navcursos = "active"
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    categories = CourseCategory.objects.all()

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    # courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "cursos", locals())

# @cache_page(60 * 15)
def curso(req, slug):
    navcursos = "active"
    curso = CourseInformation.objects.get(slug=slug)
    courses_ = CourseInformation.objects.filter(area=curso.area.pk).exclude(slug=slug)[:6]

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "curso", locals())

# @cache_page(60 * 15)
def noticias(req):
    navnoticias = "active"

    query = req.GET.get('q', '')
    paginador = Paginator( News.objects.filter(date__lte=datetime.today(), category__icontains=query).order_by("-date"), 10)    
    page_number = req.GET.get('page')
    page_obj = paginador.get_page(page_number)

    categories = News.objects.order_by('category').values_list('category', flat=True).distinct()

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "noticias", locals())

# @cache_page(60 * 15)
def noticia(req, slug):
    navnoticias = "active"
    new = News.objects.get(slug=slug)
    news = News.objects.filter(date__lte=datetime.today()).exclude(slug=slug).order_by('-date')[:6]

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "noticia", locals())

def recursos(req):
    navrecursos = "active"
    query = req.GET.get('q', '')
    paginador = Paginator( Recurso.objects.filter(access=True, tipo__icontains=query).order_by("-uploaddate"), 10)    
    page_number = req.GET.get('page')
    page_obj = paginador.get_page(page_number)
    
    categories = Recurso.objects.order_by('tipo').values_list('tipo', flat=True).distinct()

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "recursos", locals())

def release(req, slug):
    comunicado = Release.objects.get(slug=slug)
    comunicados = Release.objects.filter(publicar=True).exclude(slug=slug).order_by('-date')[:6]

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "comunicado", locals())