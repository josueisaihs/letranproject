from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from datetime import datetime

from Docencia.DatosPersonales.forms import *
from Docencia.Cursos.models import CourseInformation, Edition
from Docencia.Admision.models import Application, AnswerApplication

import Docencia.decorators as dec

TEMPLETE_PATH = "docencia/admin/%s.html"

@user_passes_test(dec.isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard(req):
    user = User.objects.get(username=req.user.username)
    teacher = TeacherPersonalInformation.objects.get(user=user.pk)
    courses = CourseInformation.objects.filter(adminteachers__pk=teacher.pk)
    try:
        edition = Edition.objects.get(
            dateinit__gte=datetime.today(), 
            dateend__gte=datetime.today()
        )

        apps = []
        for course in courses:
            for app in Application.objects.filter(edition=edition, course=course):
                apps.append(app)
        
        coursepk = courses[0].pk

        return render(
            req, TEMPLETE_PATH % "appTables", locals())
    except:
        messages.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(dec.isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard_course(req, coursepk):
    user = User.objects.get(username=req.user.username)
    teacher = TeacherPersonalInformation.objects.get(user=user.pk)
    try:
        edition = Edition.objects.get(
            dateinit__gte=datetime.today(), 
            dateend__gte=datetime.today()
        )

        courses = CourseInformation.objects.filter(adminteachers__pk=teacher.pk)

        course = CourseInformation.objects.get(pk = coursepk)
        try:
            apps = Application.objects.filter(edition=edition, course=course)

            paginador = Paginator(apps, 25)
        
            page_number = req.GET.get('page')
            page_obj = paginador.get_page(page_number)

            del apps
        except:
            messages.error(req, "No hay aplicaciones")

        VIEW = "LIST"
        
        return render(req, TEMPLETE_PATH % "appTables", locals())
    except:
        messages.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@require_POST
@user_passes_test(dec.isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard_denegar(req):
    apppk = req.POST.get("app")

    app = Application.objects.get(pk=apppk)
    app.status = "denegado"
    app.save()

    response_data = {
            'Exito': "True"
    }

    return JsonResponse(response_data) 

@require_POST
@user_passes_test(dec.isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard_accion(req):
    apppk = req.POST.get("app")
    status = req.POST.get("status")

    app = Application.objects.get(pk=apppk)
    app.status = status
    app.save()

    response_data = {
            'Exito': "True"
    }

    return JsonResponse(response_data)

@user_passes_test(dec.isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard_detail(req, coursepk):
    user = User.objects.get(username=req.user.username)
    teacher = TeacherPersonalInformation.objects.get(user=user.pk)
    try:
        edition = Edition.objects.get(
            dateinit__gte=datetime.today(), 
            dateend__gte=datetime.today()
        )

        courses = CourseInformation.objects.filter(adminteachers__pk=teacher.pk)

        course = CourseInformation.objects.get(pk = coursepk)
        try:
            apps_obj = Application.objects.filter(edition=edition, course=course)
            apps = []

            for app in apps_obj:
                answers = AnswerApplication.objects.filter(student=app.student, askApp__app__course=course.pk).order_by('askApp__order')
                app.answers = answers
                apps.append(app)

            paginador = Paginator(apps, 1)
            
            page_number = req.GET.get('page')
            page_obj = paginador.get_page(page_number)

            del apps_obj
            del answers

            VIEW = "DETAIL"
        except:
            messages.error(req, "No hay aplicaciones")    

        return render(req, TEMPLETE_PATH % "appDetail", locals())
    except:
        messages.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(dec.isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard_student_detail(req, apppk):
    user = User.objects.get(username=req.user.username)
    teacher = TeacherPersonalInformation.objects.get(user=user.pk)
    try:
        edition = Edition.objects.get(
            dateinit__gte=datetime.today(), 
            dateend__gte=datetime.today()
        )

        courses = CourseInformation.objects.filter(adminteachers__pk=teacher.pk)

        try:
            app_obj = Application.objects.get(pk = apppk)
            course = CourseInformation.objects.get(pk = app_obj.course.pk)
            coursepk = course.pk
            apps = []

            answers = AnswerApplication.objects.filter(student=app_obj.student, askApp__app__course=course.pk).order_by('askApp__order')
            app_obj.answers = answers
            apps.append(app_obj)

            paginador = Paginator(apps, 1)
            
            page_number = req.GET.get('page')
            page_obj = paginador.get_page(page_number)

            del app_obj
            del answers

            VIEW = "STUDENT"
        except:
            messages.error(req, "No hay aplicaciones")    

        return render(req, TEMPLETE_PATH % "appDetail", locals())
    except:
        messages.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")