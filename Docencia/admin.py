from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(StudentPersonalInformation, StudentPersonalInformation.Admin)
admin.site.register(TeacherPersonalInformation, TeacherPersonalInformation.Admin)
admin.site.register(Area, Area.Admin)
admin.site.register(Edition, Edition.Admin)
admin.site.register(CourseInformation, CourseInformation.Admin)
admin.site.register(EnrollmentApplication, EnrollmentApplication.Admin)
admin.site.register(AnswerApplication, AnswerApplication.Admin)
admin.site.register(OptionAskApplication, OptionAskApplication.Admin)
admin.site.register(AskApplication, AskApplication.Admin)
admin.site.register(Application, Application.Admin)
