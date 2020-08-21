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

from Docencia.Cursos.models import CourseInformation, Area, Sede
from Docencia.Index.models import HeaderIndex, News, SectionSuscribete, Suscriptor, SectionComments, Comments, Links, Events

TEMPLETE_PATH = "home/%s.html"
cantpaginator = 5

import Docencia.tasks as tasks

# @cache_page(60 * 15)
def index(request):  
    navindex = "active"
    news = News.objects.filter(date__lte=datetime.today()).order_by("-date")[:4]

    events = Events.objects.filter(date__lte=datetime.today())[:4]

    suscribete = SectionSuscribete.objects.all().first()

    seccion_coment = SectionComments.objects.all().first()

    comments = Comments.objects.all().order_by("?")[:2]

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

def eventos(req):
    naveventos = "active"
    paginador = Paginator( 
        Events.objects.filter(date__lte=datetime.today()), 
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

def evento(req, pk):
    naveventos = "active"
    event = Events.objects.get(pk=pk)
    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "evento", locals())

def cursos(req):
    navcursos = "active"
    courses = CourseInformation.objects.filter(isService=False).order_by("name")

    paginador = Paginator(courses, cantpaginator)    
    page_number = req.GET.get('page')
    page_obj = paginador.get_page(page_number)

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    # courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "cursos", locals())


def noticias(req):
    navnoticias = "active"
    paginador = Paginator( News.objects.filter(date__lte=datetime.today()), cantpaginator)    
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

    return render(req, TEMPLETE_PATH % "noticias", locals())


def noticia(req, pk):
    navnoticias = "active"
    new = News.objects.get(pk=pk)
    news = News.objects.filter(date__lte=datetime.today()).exclude(pk=pk).order_by('-date')[:6]

    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)
    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    return render(req, TEMPLETE_PATH % "noticia", locals())
