from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User

from Docencia.DatosPersonales.models import StudentPersonalInformation
from Docencia.Admision.models import Application, Edition

from datetime import datetime

import requests

def isTeacher(user):
    usermod = User.objects.filter(groups__name="Profesores", username=user.username)
    return usermod.__len__() > 0

def isStudent(user):
    usermod = User.objects.filter(groups__name="Estudiantes", username=user.username)
    return usermod.__len__() > 0
    
def isStudentAceptado(user):
    if isStudent(user):
        user_ = User.objects.get(groups__name="Estudiantes", username=user.username)
        student = StudentPersonalInformation.objects.get(user=user_.pk)
        edition = Edition.objects.get(
                dateinit__lte=datetime.today(), 
                dateend__gte=datetime.today()
                )
        # edition = Edition.objects.all().first()

        apps = Application.objects.filter(student=student, edition=edition, status="aceptado")
        return apps.__len__() > 0
    else:
        return False
        
def isStudentOrTeacher(user):
    return isTeacher(user) or isStudentAceptado(user)