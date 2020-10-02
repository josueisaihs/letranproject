from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse, HttpResponseForbidden, JsonResponse

from Docencia.DatosPersonales.forms import *
from Docencia.Cursos.models import CourseInformation, Edition, Sede, SubjectInformation
from Docencia.Admision.models import Application
from Docencia.decorators import isStudentAceptado, isTeacher
from Docencia.Plataforma.models import Class
from Docencia.Index.models import Recurso
from Docencia.Plataforma.forms import ClassForm
from Docencia.Index.forms import RecursoForm

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
                        dateinit__lte=datetime.today(), 
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
                        dateinit__lte=datetime.today(), 
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

# ******************* Profesores **********************************
@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard(req):    
        index = "active"
        user = User.objects.get(username=req.user.username)
        # try:
        teacher = TeacherPersonalInformation.objects.get(user=user.pk)
        edition = Edition.objects.get(
                dateinit__lte=datetime.today(), 
                dateend__gte=datetime.today()
                )
        
        courses = []
        coursespk_ = SubjectInformation.objects.filter(teachers=teacher.pk).order_by('course').values_list('course', flat=True).distinct()
        for pk in coursespk_:
                course = CourseInformation.objects.get(pk=pk)
                course.subjects = []
                subjects = SubjectInformation.objects.filter(teachers=teacher.pk, course=course.pk)
                for subject in subjects:
                        subject.classes = []
                        for clase in Class.objects.filter(subject=subject.pk).order_by('datepub'):
                                subject.classes.append(clase)
                        course.subjects.append(subject)
                courses.append(course)

        return render(req, TEMPLETE_PATH % "adminindex", locals())
        # except:
        #         messages.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        #         return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminclass(request, slug):
        user = User.objects.get(username=request.user.username)
        # try:
        teacher = TeacherPersonalInformation.objects.get(user=user.pk)
        edition = Edition.objects.get(
                dateinit__lte=datetime.today(), 
                dateend__gte=datetime.today()
                )
        
        courses = []
        coursespk_ = SubjectInformation.objects.filter(teachers=teacher.pk).order_by('course').values_list('course', flat=True).distinct()
        for pk in coursespk_:
                course = CourseInformation.objects.get(pk=pk)
                course.subjects = []
                subjects = SubjectInformation.objects.filter(teachers=teacher.pk, course=course.pk)
                for subject in subjects:
                        subject.classes = []
                        for clase in Class.objects.filter(subject=subject.pk).order_by('datepub'):
                                subject.classes.append(clase)
                        course.subjects.append(subject)
                courses.append(course)

        subject = SubjectInformation.objects.get(slug=slug)
        if request.method == "POST":
                form = ClassForm(request.POST)
                if form.is_valid():
                        class_ = form.save()

                        recursos = []
                        for filename in form.cleaned_data['recursosjson']['name']:
                                recursos.append(Recurso.objects.get(name=filename))
                        if recursos.__len__() > 0:
                                class_.resources.set(recursos)
                        else:
                                class_.resources.clear()
                        return HttpResponseRedirect('/plataforma/admin/dashboard/')
        else:
                form = ClassForm()
        return render(request, TEMPLETE_PATH % "adminclass", locals())
        # except:
        #         messages.error(request, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        #         return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

def uploadfile(req):
        if req.is_ajax():
                form = RecursoForm(req.POST, files=req.FILES)
                if form.is_valid():
                        form.save()

                        return JsonResponse({'response': True})
                else:
                        return JsonResponse({"response": False})
        else: 
                return HttpResponseForbidden()

def deletefile(req):
        if req.is_ajax():
                Recurso.objects.get(req.POST.get("slug")).delete()
                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminclass_edit(request, slug, slugclass):
        user = User.objects.get(username=request.user.username)
        # try:
        teacher = TeacherPersonalInformation.objects.get(user=user.pk)
        edition = Edition.objects.get(
                dateinit__lte=datetime.today(), 
                dateend__gte=datetime.today()
                )
        
        courses = []
        coursespk_ = SubjectInformation.objects.filter(teachers=teacher.pk).order_by('course').values_list('course', flat=True).distinct()
        for pk in coursespk_:
                course = CourseInformation.objects.get(pk=pk)
                course.subjects = []
                subjects = SubjectInformation.objects.filter(teachers=teacher.pk, course=course.pk)
                for subject in subjects:
                        subject.classes = []
                        for clase in Class.objects.filter(subject=subject.pk).order_by('datepub'):
                                subject.classes.append(clase)
                        course.subjects.append(subject)
                courses.append(course)

        edit = True
        subject = SubjectInformation.objects.get(slug=slug)
        class_edit = Class.objects.get(slug=slugclass)
        if request.method == "POST":
                form = ClassForm(request.POST, instance=class_edit)
                if form.is_valid():
                        class_ = form.save()

                        recursos = []
                        for filename in form.cleaned_data['recursosjson']['name']:
                                recursos.append(Recurso.objects.get(name=filename))
                        if recursos.__len__() > 0:
                                class_.resources.set(recursos)
                        else:
                                class_.resources.clear()
                        return HttpResponseRedirect('/plataforma/admin/dashboard/')
        else:
                form = ClassForm(instance=class_edit)
        return render(request, TEMPLETE_PATH % "adminclass", locals())
        # except:
        #         messages.error(request, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        #         return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")