from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(StudentPersonalInformation, StudentPersonalInformation.Admin)
admin.site.register(TeacherPersonalInformation, TeacherPersonalInformation.Admin)
admin.site.register(Colaboradores, Colaboradores.Admin)
admin.site.register(Area, Area.Admin)
admin.site.register(Edition, Edition.Admin)
admin.site.register(Sede, Sede.Admin)
admin.site.register(CourseInformation, CourseInformation.Admin)
admin.site.register(CourseSchedule, CourseSchedule.Admin)
admin.site.register(EnrollmentApplication, EnrollmentApplication.Admin)
admin.site.register(AnswerApplication, AnswerApplication.Admin)
admin.site.register(OptionAskApplication, OptionAskApplication.Admin)
admin.site.register(AskApplication, AskApplication.Admin)
admin.site.register(Application, Application.Admin)
admin.site.register(Suscriptor, Suscriptor.Admin)
admin.site.register(News, News.Admin)
admin.site.register(Post, Post.Admin)
admin.site.register(Events, Events.Admin)
admin.site.register(EventsDate, EventsDate.Admin)
admin.site.register(HeaderIndex, HeaderIndex.Admin)
admin.site.register(SectionSuscribete, SectionSuscribete.Admin)
admin.site.register(SectionComments, SectionComments.Admin)
admin.site.register(Comments, Comments.Admin)
admin.site.register(Links, Links.Admin)
admin.site.register(RespuestasError, RespuestasError.Admin)