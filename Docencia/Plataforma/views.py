from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages as messagesdj
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from Docencia.DatosPersonales.forms import *
from Docencia.Cursos.models import CourseInformation, Edition, Sede, SubjectInformation, GroupInformation
from Docencia.Admision.models import Application
from Docencia.decorators import isStudentAceptado, isTeacher
from Docencia.Plataforma.models import Class, Message
from Docencia.Index.models import Recurso
from Docencia.Plataforma.forms import ClassForm
from Docencia.Index.forms import RecursoForm

from Docencia.tasks import enviar_comunicado

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
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()

                apps = Application.objects.filter(student=student, edition=edition, status="aceptado")
                if apps.__len__() > 0:
                        for app in apps:
                                app.course.subjects = []
                                for subject in SubjectInformation.objects.filter(course=app.course.pk):
                                        app.course.subjects.append(subject)
                                        del subject
                                del app

                        return render(req, TEMPLETE_PATH % "index", locals())
                else:
                        messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                        return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def curso(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()

                apps = Application.objects.filter(student=student, edition=edition, status="aceptado")
                if apps.__len__() > 0:
                        for app in apps:
                                app.course.subjects = []
                                for subject in SubjectInformation.objects.filter(course=app.course.pk):
                                        app.course.subjects.append(subject)
                                        del subject
                                del app
                        
                        course = CourseInformation.objects.get(slug=slug)
                        course.subjects = []
                        for subject in SubjectInformation.objects.filter(course=course.pk):
                                course.subjects.append(subject)
                                del subject

                        return render(req, TEMPLETE_PATH % "curso", locals())
                else:
                        messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                        return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def subject(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()

                apps = Application.objects.filter(student=student, edition=edition, status="aceptado")
                if apps.__len__() > 0:
                        for app in apps:
                                app.course.subjects = []
                                for subject in SubjectInformation.objects.filter(course=app.course.pk):
                                        app.course.subjects.append(subject)
                                        del subject

                                app.course.recursos = []
                                for recurso in Recurso.objects.filter(courses=app.course.pk):
                                        app.course.recursos.append(recurso)
                                        del recurso
                        
                        for subject in SubjectInformation.objects.filter(slug=slug):
                                        subject.classes = []
                                        for clase in Class.objects.filter(subject=subject.pk, datepub__lte=datetime.today()).order_by('-datepub'):
                                                subject.classes.append(clase)

                        return render(req, TEMPLETE_PATH % "subject", locals())
                else:
                        messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                        return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")


@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def clase(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()

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
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

def recursos(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()

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
                                del app
                        
                        course = CourseInformation.objects.get(slug=slug)
                        course.recursos = []
                        for recurso in Recurso.objects.filter(courses=course.pk):
                                course.recursos.append(recurso)

                        return render(req, TEMPLETE_PATH % "recursos", locals())
                else:
                        messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                        return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")


@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def downloadResource(req, slug):
        resource = Recurso.objects.get(slug=slug)
        return FileResponse(open(resource.recurso.file.__str__(), 'rb'))

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def messages(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()

                apps = Application.objects.filter(student=student, edition=edition, status="aceptado")
                for app in apps:
                        app.course.subjects = []
                        for subject in SubjectInformation.objects.filter(course=app.course.pk):
                                subject.classes = []
                                for clase in Class.objects.filter(subject=subject.pk, datepub__lte=datetime.today()).order_by('datepub'):
                                        subject.classes.append(clase)
                                app.course.subjects.append(subject)
                return render(req, TEMPLETE_PATH % "messages", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")
        

# ******************* Profesores **********************************
@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard(req):    
        index = "active"
        user = User.objects.get(username=req.user.username)
        # try:
        teacher = TeacherPersonalInformation.objects.get(user=user.pk)
        try:
                edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
        except ObjectDoesNotExist:
                edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()
        
        courses = CourseInformation.obejcts.filter(edition=edition.pk, teacher=)

        return render(req, TEMPLETE_PATH % "adminindex", locals())
        # except:
        #         messagesdj.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
        #         return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admincourse(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                teacher = TeacherPersonalInformation.objects.get(user=user.pk)                
                course = CourseInformation.objects.get(slug=slug)

                return render(req, TEMPLETE_PATH % "admincurso", locals())
        except:
                messagesdj.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminsubject(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                teacher = TeacherPersonalInformation.objects.get(user=user.pk)                
                subject =SubjectInformation.objects.get(slug=slug)

                return render(req, TEMPLETE_PATH % "adminsubject", locals())
        except:
                messagesdj.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")


@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminclass(request, slug):
        user = User.objects.get(username=request.user.username)
        try:
                teacher = TeacherPersonalInformation.objects.get(user=user.pk)
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
        except:
                messagesdj.error(request, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

def uploadfile(req):
        if req.is_ajax():
                form = RecursoForm(req.POST, files=req.FILES)
                if form.is_valid():
                        recurso = form.save()

                        return JsonResponse({'response': True, 'slug': recurso.slug})
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
def adminclass_edit(request, slug):
        user = User.objects.get(username=request.user.username)
        try:
                edit = True
                class_edit = Class.objects.get(slug=slug)
                subject = SubjectInformation.objects.get(pk=class_edit.subject.pk)
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
        except:
                messagesdj.error(request, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def deleteclass(req):
        if req.is_ajax():
                Class.objects.get(slug=req.POST.get("slug")).delete()
                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def sendmasivemail(req):
        if req.is_ajax():
                course = CourseInformation.objects.get(slug=req.POST.get('courseslug'))
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()

                enviar_comunicado(edition.pk, course.pk, req.POST.get('subject'), req.POST.get('body'))

                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def downloadTeacherResource(req, slug):
        resource = Recurso.objects.get(slug=slug)
        return FileResponse(open(resource.recurso.file.__str__(), 'rb'))

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminmessages(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                teacher = TeacherPersonalInformation.objects.get(user=user.pk)
                try:
                        edition = Edition.objects.get(dateinit__lte=datetime.today(), dateend__gte=datetime.today())
                except ObjectDoesNotExist:
                        edition = Edition.objects.filter(dateend__gte=datetime.today()).order_by('dateinit', 'dateend').first()
                
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

                                # Cargando los recursos del curso
                                course.recursos = []
                                for recurso in Recurso.objects.filter(courses=course.pk):
                                        course.recursos.append(recurso)

                        courses.append(course)
                return render(req, TEMPLETE_PATH % "messages", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

def send_message(req):
        if req.is_ajax():
                message = Message(
                        user=User.objects.get(
                                pk=req.user.pk
                        ),
                        subject=SubjectInformation.objects.get(
                                slug=req.POST.get('subjectslug')
                        ),
                        body=req.POST.get('msg'),
                        edition=Edition.objects.get(
                                dateinit__lte=datetime.today(), 
                                dateend__gte=datetime.today()
                        )
                )
                message.save()

                return JsonResponse({'response': True, 'slug': message.slug})
        else:
                return JsonResponse({'response': False})

def update_messages(req):
        if req.is_ajax():
                edition = Edition.objects.get(
                        dateinit__lte=datetime.today(), 
                        dateend__gte=datetime.today()
                )
                messages = Message.objects.filter(
                        subject=SubjectInformation.objects.get(slug=req.POST.get('subjectslug')), 
                        edition=edition,
                        approved=True
                )
                color = ('text-warning', 'text-info', 'text-white-50', 'text-success')

                return JsonResponse({'data': serializers.serialize('json', messages)})
        else:
                return JsonResponse({'data': False})

def delete_message(req):
        Message.objects.get(slug=req.POST.get("slug")).delete()

        return JsonResponse({"response": True})

def user_message(req):
        if req.is_ajax():
                user = User.objects.get(pk=req.POST.get('userpk'))
                if (user.first_name != "" and user.last_name != ""): 
                        sal = "%s %s" % (user.first_name, user.last_name) 
                else: 
                        sal = user.username

                return JsonResponse({'response': sal})

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def creategroup(req):
        if req.is_ajax():
                teacher = TeacherPersonalInformation.objects.get(user=req.user.pk)
                group = GroupInformation(
                        name=req.POST.get('name'),
                        edition=Edition.objects.get(
                                dateinit__lte=datetime.today(), 
                                dateend__gte=datetime.today()
                        ),
                        course=CourseInformation.objects.get(slug=req.POST.get('course')),
                )
                group.save()
                group.teachers.set([teacher,])
                group.save()
                return JsonResponse({'response': True})
