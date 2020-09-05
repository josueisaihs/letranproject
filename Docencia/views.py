from .models import RespuestasError
from django.template import RequestContext
from django.shortcuts import render

import Docencia.Admin.views as admon
import Docencia.Admision.views as admision
import Docencia.DatosPersonales.views as datospersonales
import Docencia.Index.views as index
import Docencia.Plataforma.views as plataforma

#...
#404: página no encontrada
def pag_404_not_found(request, exception):
    # Requeridos en todo el Index
    header = index.HeaderIndex.objects.get(isVisible=True)

    areas = index.Area.objects.all().order_by("name")
    courses = index.CourseInformation.objects.filter(isService=False).order_by("name")
    services = index.CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = index.Sede.objects.get(isprincipal=True)

    enl = index.Links.objects.filter(section="enl").order_by("name")
    pre = index.Links.objects.filter(section="opr").order_by("name")

    respuesta = RespuestasError.objects.order_by('?').first()
    return render(request, "home/404.html", locals())
 
#500: error en el servidor
def pag_500_error_server(request):
    # Requeridos en todo el Index
    header = index.HeaderIndex.objects.get(isVisible=True)

    areas = index.Area.objects.all().order_by("name")
    courses = index.CourseInformation.objects.filter(isService=False).order_by("name")
    services = index.CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = index.Sede.objects.get(isprincipal=True)

    enl = index.Links.objects.filter(section="enl").order_by("name")
    pre = index.Links.objects.filter(section="opr").order_by("name") 

    respuesta = RespuestasError.objects.order_by('?').first()
    return render(request, "home/500.html", locals())

def pag_403_permission_denied(request, exception):
    # Requeridos en todo el Index
    header = index.HeaderIndex.objects.get(isVisible=True)

    areas = index.Area.objects.all().order_by("name")
    courses = index.CourseInformation.objects.filter(isService=False).order_by("name")
    services = index.CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = index.Sede.objects.get(isprincipal=True)

    enl = index.Links.objects.filter(section="enl").order_by("name")
    pre = index.Links.objects.filter(section="opr").order_by("name") 

    respuesta = RespuestasError.objects.order_by('?').first()
    return render(request, 'home/403.html', locals())

def politicaprivacidad(req):
     # Requeridos en todo el Index
    header = index.HeaderIndex.objects.get(isVisible=True)

    areas = index.Area.objects.all().order_by("name")
    courses = index.CourseInformation.objects.filter(isService=False).order_by("name")
    services = index.CourseInformation.objects.filter(isService=True).order_by("name")
    
    sede = index.Sede.objects.get(isprincipal=True)

    enl = index.Links.objects.filter(section="enl").order_by("name")
    pre = index.Links.objects.filter(section="opr").order_by("name") 
    return render(req, "home/politica.html", locals())
