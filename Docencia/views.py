from django.shortcuts import render

from Docencia.DatosPersonales.views import *
from Docencia.Admision.views import *
from Docencia.Admin.views import *
from Docencia.Index.views import *

from django.template import RequestContext
from django.shortcuts import render
#...
#404: página no encontrada
def pag_404_not_found(request, exception):
    return render(request, "404.html")
 
#500: error en el servidor
def pag_500_error_server(request):
    return render(request, "500.html")
