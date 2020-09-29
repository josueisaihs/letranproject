from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse

from Docencia.DatosPersonales.forms import *
from Docencia.Cursos.models import CourseInformation, Edition, Sede, SubjectInformation
from Docencia.Admision.models import Application
from Docencia.decorators import isStudentAceptado
from Docencia.Plataforma.models import Class
from Docencia.Index.models import Recurso

from Docencia.Plataforma.forms import ClassForm

from datetime import datetime
import mimetypes

TEMPLETE_PATH = "docencia/plataforma/%s.html"

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def dashboard(req):    
        index = "active"
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                edition = Edition.objects.get(
                        dateinit__gte=datetime.today(), 
                        dateend__gte=datetime.today()
                        )

                apps = Application.objects.filter(student=student, edition=edition, status="aceptado")
                if apps.__len__() > 0:
                        for app in apps:
                                app.course.subjects = []
                                for subject in SubjectInformation.objects.filter(course=app.course.pk):
                                        subject.classes = []
                                        for clase in Class.objects.filter(subject=subject.pk, datepub__lte=datetime.today()).order_by('datepub'):
                                                subject.classes.append(clase)
                                        app.course.subjects.append(subject)
                        del subject
                        del clase
                        del app
                        del edition

                        return render(req, TEMPLETE_PATH % "index", locals())
                else:
                        messages.error(req, "Este usuario no tiene acceso a este servicio")
                        return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")
        except:
                messages.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")


@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def clase(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                edition = Edition.objects.get(
                        dateinit__gte=datetime.today(), 
                        dateend__gte=datetime.today()
                        )

                apps = Application.objects.filter(student=student, edition=edition, status="aceptado")
                for app in apps:
                        app.course.subjects = []
                        for subject in SubjectInformation.objects.filter(course=app.course.pk):
                                subject.classes = []
                                for clase in Class.objects.filter(subject=subject.pk, datepub__lte=datetime.today()).order_by('datepub'):
                                        subject.classes.append(clase)
                                app.course.subjects.append(subject)

                del subject
                del clase
                del app
                del edition

                clase = Class.objects.get(slug=slug)
                return render(req, TEMPLETE_PATH % "clase", locals())
        except:
                messages.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")


@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def downloadResource(req, slug):
        resource = Recurso.objects.get(slug=slug)
        return FileResponse(open(resource.recurso.file.__str__(), 'rb'))
        # fl_path = '/file/path'
        # filename = 'downloaded_file_name.extension'
        # resource = Recurso.objects.get(slug=slug)
        # fl_path = resource.recurso.file.__str__()

        # fl = open(fl_path, 'rb')
        # mime_type, _ = mimetypes.guess_type(fl_path)
        # response = HttpResponse(fl, content_type=mime_type)
        # response['Content-Disposition'] = "attachment; filename=%s" % resource.name
        # return response

def createclass(req):
        return render(req, TEMPLETE_PATH % "classform", locals())        