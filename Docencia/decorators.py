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