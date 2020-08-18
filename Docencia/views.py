from django.shortcuts import render

from Docencia.DatosPersonales.views import *
from Docencia.Admision.views import *
from Docencia.Admin.views import *
from Docencia.Index.views import *

from django.views.defaults import page_not_found

#404: página no encontrada
def pag_404_not_found(request, exception):
    return page_not_found(request, "error/404.html")
