from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import *
from django.conf import settings
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from datetime import datetime, date

from Docencia.DatosPersonales.models import StudentPersonalInformation
from Docencia.Cursos.models import CourseInformation, Edition
from Docencia.Admision.models import *

TEMPLETE_PATH = "docencia/admision/%s.html"

@login_required(login_url="/login/", redirect_field_name="next")
def selectcourse(req):
    courses = CourseInformation.objects.filter(openregistre__lte=datetime.today(),
                                deadline__gte=datetime.today())

    editions = Edition.objects.all()    
    
    # Eliminando los cursos a los que ha aplicado
    user = User.objects.get(username=req.user.username)
    student = StudentPersonalInformation.objects.get(user=user.pk)

    edition = Edition.objects.get(
            dateinit__gte=datetime.today(), 
            dateend__gte=datetime.today())

    appls = Application.objects.filter(student=student.pk, edition=edition.pk)
    for appl in appls:
        courses = courses.exclude(pk=appl.course.pk)
        
        if len(courses) == 0:
            messages.warning(req, "Ha aplicado a todos los cursos disponibles")

    return render(req, TEMPLETE_PATH % "selectcourse", locals())

@login_required(login_url="/login/", redirect_field_name="next")
def application(req, coursePk):
    course = CourseInformation.objects.get(pk=coursePk)
    
    try:
        enrollement = EnrollmentApplication.objects.get(course=coursePk)
        askApplication = []
    
        for ask in AskApplication.objects.filter(app=enrollement).order_by('order'):
            if ask.askType == "o" or ask.askType == "r":
                ask.options = OptionAskApplication.objects.filter(askApp=ask.pk)
            askApplication.append(ask)
    except ObjectDoesNotExist as e:
        # Si el curso no tiene Preguntas de Admisión se generá una aplicación automatica
        user = User.objects.get(username=req.user.username)
        student = StudentPersonalInformation.objects.get(user=user.pk)
        
        course = CourseInformation.objects.get(pk=coursePk)

        edition = Edition.objects.get(
            dateinit__gte=datetime.today(), 
            dateend__gte=datetime.today())
                
        try:
            app = Application()
            app.student = student
            app.course = course
            app.edition = edition
            app.save()
        except IntegrityError as e:
            Application.objects.filter(course=course.pk, student=student.pk, edition=edition.pk).delete()
            app.save()

        messages.success(req, "Aplicación enviada a %s" % course.name)
        return HttpResponseRedirect('/admision/dashboard/')

    return render(req, TEMPLETE_PATH % "formapp", locals())

@require_POST
def applicationAjax(req):
    user = User.objects.get(username=req.user.username)
    student = StudentPersonalInformation.objects.get(user=user.pk)

    askPk = req.POST.get('ask')
    askType = req.POST.get('askType')
    answer = req.POST.get('answer')

    try:
        if askType == "o" or askType == "r":
            answer = OptionAskApplication.objects.get(pk=answer).option

        answerApp = AnswerApplication()
        answerApp.askApp = AskApplication.objects.get(pk=askPk)
        answerApp.student = student
        answerApp.answer = answer

        enrollment = EnrollmentApplication.objects.get(pk=answerApp.askApp.app.pk)
        course = CourseInformation.objects.get(pk=enrollment.course.pk)

        edition = Edition.objects.get(
            dateinit__gte=datetime.today(), 
            dateend__gte=datetime.today())
                
        try:
            app = Application()
            app.student = student
            app.course = course
            app.edition = edition
            app.save()
        except IntegrityError as e:
            Application.objects.filter(course=course.pk, student=student.pk, edition=edition.pk).delete()
            app.save()

        try:
            answerApp.save()

            messages.success(req, "Aplicación enviada a %s" % enrollment.course.name)

            response_data = {
                'Exito': "True"
            }
        except IntegrityError as e:
            response_data = {
                'Exito': "True"
            }
            AnswerApplication.objects.filter(askApp=askPk, student=student.pk).delete()
            answerApp.save()

            messages.success(req, "Nueva Aplicación enviada a %s\nSe eliminó su aplicación anterior" % enrollment.course.name)            
    except ValueError as e:
        response_data = {
            'Exito': "False"
        }

    return JsonResponse(response_data)    
# <> fin applicationAjax


@require_POST
def applicationCancelAjax(req):
    user = User.objects.get(username=req.user.username)
    student = StudentPersonalInformation.objects.get(user=user.pk)

    appPk = req.POST.get('app');

    Application.objects.get(pk=appPk).delete()

    response_data = {
            'Exito': "True"
    }
    return JsonResponse(response_data)