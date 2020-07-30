from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404

from hashlib import blake2s
from datetime import datetime
from random import randrange

from validate_email import validate_email

from Docencia.DatosPersonales.forms import *
from Docencia.Cursos.models import CourseInformation, Edition
from Docencia.Admision.models import Application


TEMPLETE_PATH = "docencia/admision/%s.html"

@login_required(login_url="/login/", redirect_field_name="next")
def dashboard(req):
    courses = CourseInformation.objects.filter(openregistre__lte=datetime.today(),
                                deadline__gte=datetime.today())
    
    user = User.objects.get(username=req.user.username)
    try:
        student = StudentPersonalInformation.objects.get(user=user.pk)
        edition = Edition.objects.get(
                dateinit__gte=datetime.today(), 
                dateend__gte=datetime.today())

        apps = Application.objects.filter(student=student, edition=edition)
        if (len(courses) > 0):
            messages.add_message(req, settings.MESSAGES_INFO, courses[0].deadline.strftime("%d de %b"))
        del courses

        return render(
            req, TEMPLETE_PATH % "dashboard", locals())
    except:
        raise Http404("No existe")

def registro(req):
    if req.method == "POST":
        form = StudentPersonalInformationForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            lastname = form.cleaned_data["lastname"]
            username = form.cleaned_data["email"]

            hash = blake2s(bytes(username, "UTF-8"), key=bytes("%s" % randrange(1000, 9999), "UTF-8"), digest_size=2)
            pwd = "{}".format(hash.hexdigest())       

            email = EmailMessage(
                "Centro Fray Bartolomé de las Casas", 
                "%s %s,\nSu cuenta ha sido creada en el CFBC.\nUsuario: %s\nContraseña: %s\n\nPara continuar siga el siguiente enlace:\n%s" % (name, lastname, username, pwd, "http://localhost:8000/admision/dashboard/"), 
                to=[username],
            )

            try:
                # if validate_email(username, verify=True):
                if (True):
                    email.send(fail_silently=False)

                    form.save()
                    
                    student = StudentPersonalInformation.objects.get(email=username)
                    student.user.set_password(pwd)
                    student.user.save()
                    student.save()

                    return HttpResponseRedirect('/admision/success/')  
                else:  
                    messages.error(req, "La cuenta de correo no existe") 
            except TimeoutError as e:
                messages.error(req, "Tiempo de Espera agotado.")
    else:
        form = StudentPersonalInformationForm()

    return render(req, TEMPLETE_PATH % "form", locals())

def registrocompletado(req):
    return render(req, TEMPLETE_PATH % "success", locals())