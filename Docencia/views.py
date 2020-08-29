from .models import RespuestasError
from django.template import RequestContext
from django.shortcuts import render

from Docencia.Admin.views import *
from Docencia.Admision.views import *
from Docencia.DatosPersonales.views import *
from Docencia.Index.views import *
from Docencia.Plataforma.views import *

#...
#404: página no encontrada
def pag_404_not_found(request, exception):
    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)

    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name")

    respuesta = RespuestasError.objects.order_by('?').first()
    return render(request, "home/404.html", locals())
 
#500: error en el servidor
def pag_500_error_server(request):
    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)

    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    respuesta = RespuestasError.objects.order_by('?').first()
    return render(request, "home/500.html", locals())

def pag_403_permission_denied(request, exception):
    # Requeridos en todo el Index
    header = HeaderIndex.objects.get(isVisible=True)

    areas = Area.objects.all().order_by("name")
    courses = CourseInformation.objects.filter(isService=False).order_by("name")
    services = CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = Sede.objects.get(isprincipal=True)

    enl = Links.objects.filter(section="enl").order_by("name")
    pre = Links.objects.filter(section="opr").order_by("name") 

    respuesta = RespuestasError.objects.order_by('?').first()
    return render(request, 'home/403.html', locals())
