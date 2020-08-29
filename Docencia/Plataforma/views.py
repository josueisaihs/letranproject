from django.shortcuts import render

from Docencia.Plataforma.models import Class

TEMPLETE_PATH = "docencia/plataforma/%s.html"

def clase(req):
    clase = Class.objects.order_by("?").first()

    return render(req, TEMPLETE_PATH % "clase", locals())
