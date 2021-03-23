from django import template
from django.db.models import Q
import re

register = template.Library()

from Docencia.Cursos.models import CourseInformation
from Docencia.Plataforma.models import HomeWork

@register.simple_tag
def device_is_mobile(request):
    try:
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
        return True if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']) else False
    except:
        return False

@register.filter
def teacher(value, arg):
    return value.filter(teachers__id=arg)

@register.filter
def subject(value, arg):
    return value.get(slug=arg)

@register.simple_tag
def adminTeacher(courseSlug, teacherPk):
    return CourseInformation.objects.filter(slug=courseSlug, adminteachers__id=teacherPk).exists()

@register.filter
def getOptativas(value):
    return value.filter(Q(mode="Optativa") | Q(mode="Libre Elección"))

@register.filter
def getObligatorias(value):
    return value.filter(Q(mode="Obligatoria") | Q(mode="Troncal"))

''' @register.simple_tag(takes_context=True)
def getHomeWorks(subjectSlug, studentPk):
    return HomeWork.objects.filter() '''


