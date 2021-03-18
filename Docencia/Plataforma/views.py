from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib import messages as messagesdj
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import StreamingHttpResponse

from Docencia.DatosPersonales.forms import *
from Docencia.Cursos.models import CourseInformation, Edition, Sede, SubjectInformation 
from Docencia.Admision.models import Application
from Docencia.decorators import isStudentAceptado, isTeacher, isStudentOrTeacher
from Docencia.Plataforma.models import Class, Message, Enrollment, Assistence, RoomClass, GroupInformation, HomeWork
from Docencia.Index.models import Recurso
from Docencia.Plataforma.forms import ClassForm, HomeWorkForm
from Docencia.Index.forms import RecursoForm

from Docencia.tasks import enviar_comunicado, enviar_notification

import csv
from datetime import datetime
import mimetypes
from json import loads

TEMPLETE_PATH = "docencia/plataforma/%s.html"

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def dashboard(req):    
        index = "active"
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
               
                apps = Application.objects.filter(student=student, edition__active=True, status="aceptado")
                return render(req, TEMPLETE_PATH % "index", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def curso(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                enrollments = Enrollment.objects.filter(student__pk=student.pk, edition__active=True, subject__course__slug=slug)
                if enrollments.__len__() > 0:
                        apps = Application.objects.filter(student=student, edition__active=True, status="aceptado")
                        app = Application.objects.get(student=student, edition__active=True, status="aceptado", course__slug=slug)
                        return render(req, TEMPLETE_PATH % "curso", locals())
                else:
                        # En caso que no esté matriculado en ninguna asignatura, se redirecciona a la vista para matricula
                        return redirect('plataforma_enrollment', slug)
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def subject(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                apps = Application.objects.filter(student=student, edition__active=True, status="aceptado")
                subject = SubjectInformation.objects.get(slug=slug)
                return render(req, TEMPLETE_PATH % "subject", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")


@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def clase(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                apps = Application.objects.filter(student=student, edition__active=True, status="aceptado")
                clase = Class.objects.get(slug=slug)
                return render(req, TEMPLETE_PATH % "clase", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def homework(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)
                apps = Application.objects.filter(student=student, edition__active=True, status="aceptado")
                clase = Class.objects.get(slug=slug)
                edition = Edition.objects.get(active=True)

                if req.method == "POST":
                        form = HomeWorkForm(req.POST, req.FILES)
                        if form.is_valid():
                                form.save()

                                return redirect('plataforma_clase', slug)
                else:
                        form = HomeWorkForm()                

                return render(req, TEMPLETE_PATH % "homework", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def homeworks(req, slug):
        user = User.objects.get(username=req.user.username)
        student = StudentPersonalInformation.objects.get(user=user.pk)
        apps = Application.objects.filter(student=student, edition__active=True, status="aceptado")
        app = Application.objects.get(student=student, edition__active=True, status="aceptado", course__slug=slug)

        try:
                homeworks = HomeWork.objects.filter(
                        edition__active=True, 
                        student=student,
                        clase__subject__course__slug=slug).order_by('-datepub')
                paginador = Paginator(homeworks, 25)

                page_number = req.GET.get('page')
                page_obj = paginador.get_page(page_number)

                del homeworks
        except:
                messages.error("No hay tareas para mostrar")

        return render(req, TEMPLETE_PATH % "homeworks", locals())

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

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def enrollment(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                student = StudentPersonalInformation.objects.get(user=user.pk)          
                apps = Application.objects.filter(student=student, edition__active=True, status="aceptado")
                app = Application.objects.get(student=student, edition__active=True, status="aceptado", course__slug=slug)
                return render(req, TEMPLETE_PATH % "enrollment", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")      

@user_passes_test(isStudentAceptado, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def apienrollment(req):
        user = User.objects.get(username=req.user.username)
        if req.is_ajax():
                edition = Edition.objects.get(active=True)
                student = StudentPersonalInformation.objects.get(user=user.pk)

                for subjectpk in loads(req.POST.get('datos[]')):
                        enrollment = Enrollment()
                        enrollment.edition = edition
                        enrollment.subject = SubjectInformation.objects.get(pk=subjectpk)
                        enrollment.student = student

                        enrollment.save()
                
                for subject in SubjectInformation.objects.filter(Q(mode="Obligatoria") | Q(mode="Troncal"), course__slug = req.POST.get('course')):
                        enrollment = Enrollment()
                        enrollment.edition = edition
                        enrollment.subject = subject
                        enrollment.student = student

                        enrollment.save()
                
                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

# ******************* Profesores **********************************
@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admindashboard(req):    
        index = "active"
        try:
                teacher = TeacherPersonalInformation.objects.get(user=User.objects.get(username=req.user.username))
                courses = teacher.getCourses()

                return render(req, TEMPLETE_PATH % "adminindex", locals())
        except:
                messagesdj.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

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
                                return redirect('plataforma_admin_subject', slug)
                else:
                        form = ClassForm()
                return render(request, TEMPLETE_PATH % "adminclass", locals())
        except:
                messagesdj.error(request, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminclass_edit(request, slug):
        user = User.objects.get(username=request.user.username)
        try:
                edit = True
                class_edit = Class.objects.get(slug=slug)
                subject = SubjectInformation.objects.get(slug=class_edit.subject.slug)                
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
                                return redirect('plataforma_admin_subject', subject.slug)
                else:
                        form = ClassForm(instance=class_edit)
                return render(request, TEMPLETE_PATH % "adminclass", locals())
        except:
                messages.error(request, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def creategroup(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                teacher = TeacherPersonalInformation.objects.get(user=user.pk)                
                course = CourseInformation.objects.get(slug=slug)

                return render(req, TEMPLETE_PATH % "admingroups", locals())
        except:
                messagesdj.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def createcomunicate(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                teacher = TeacherPersonalInformation.objects.get(user=user.pk)                
                course = CourseInformation.objects.get(slug=slug)

                return render(req, TEMPLETE_PATH % "admincomunicado", locals())
        except:
                messagesdj.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminrecursos(req, slug):
        user = User.objects.get(username=req.user.username)
        try:
                teacher = TeacherPersonalInformation.objects.get(user=user.pk)                
                course = CourseInformation.objects.get(slug=slug)

                return render(req, TEMPLETE_PATH % "adminrecurso", locals())
        except:
                messagesdj.error(req, "Ha ocurrido un error interno o este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/admin/dashboard/")

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def downloadAdminResource(req, slug):
        resource = Recurso.objects.get(slug=slug)
        return FileResponse(open(resource.recurso.file.__str__(), 'rb'))

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def deleteAdminResource(req, slug, slugclass):
        resource = Recurso.objects.get(slug=slug)
        resource.delete()
        return HttpResponseRedirect('/plataforma/admin/dashboard/curso/recursos/%s' % slugclass)

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
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

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def deletefile(req):
        if req.is_ajax():
                Recurso.objects.get(req.POST.get("slug")).delete()
                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

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
                return render(req, TEMPLETE_PATH % "adminmessages", locals())
        except:
                messagesdj.error(req, "Este usuario no tiene acceso a este servicio")
                return HttpResponseRedirect("/login/?next=/plataforma/dashboard/")

@user_passes_test(isStudentOrTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
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
                return HttpResponseForbidden()

@user_passes_test(isStudentOrTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def send_message_audio(req):
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
                return HttpResponseForbidden()

@user_passes_test(isStudentOrTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
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
                return HttpResponseForbidden()

@user_passes_test(isStudentOrTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def delete_message(req):
        Message.objects.get(slug=req.POST.get("slug")).delete()

        return JsonResponse({"response": True})

@user_passes_test(isStudentOrTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def user_message(req):
        if req.is_ajax():
                user = User.objects.get(pk=req.POST.get('userpk'))
                if (user.first_name != "" and user.last_name != ""): 
                        sal = "%s %s" % (user.first_name, user.last_name) 
                else: 
                        sal = user.username

                return JsonResponse({'response': sal})
        else: 
                return HttpResponseForbidden()

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def apicreategroup(req):
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
        else: 
                return HttpResponseForbidden()

#todo
@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def admingroup(req, grupo):
        group = GroupInformation.objects.get(slug=grupo)
        return render(req, TEMPLETE_PATH % 'admingroup', locals())

#todo
@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminassistence(req, slug):
        subject = SubjectInformation.objects.get(slug=slug)
        enrollments = Enrollment.objects.filter(subject__slug=slug)
        rooms = RoomClass.objects.all()
        return render(req, TEMPLETE_PATH % 'adminassistence', locals())

#todo
@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def apiassistence(req):
        if req.is_ajax():
                try:
                        assistence = Assistence.objects.get(enrollment__slug=req.POST.get('enrollment'))
                        assistence.delete()
                except ObjectDoesNotExist:
                        pass
                assistence = Assistence()
                assistence.enrollment = Enrollment.objects.get(slug=req.POST.get('enrollment'))                
                assistence.roomclass = RoomClass.objects.get(slug=req.POST.get('roomclass'))
                assistence.status = req.POST.get('status')
                assistence.save()

                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminstudentslist(req, slug):
        user = User.objects.get(username=req.user.username)
        teacher = TeacherPersonalInformation.objects.get(user=user.pk)
        
        course = CourseInformation.objects.get(slug=slug)
        applications = Application.objects.filter(edition__active=True, course__slug=slug, status="aceptado")

        return render(req, TEMPLETE_PATH % "adminstudents", locals())

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminnotification(req, slug, pk):
        user = User.objects.get(username=req.user.username)
        teacher = TeacherPersonalInformation.objects.get(user=user.pk)

        course = CourseInformation.objects.get(slug=slug)
        student = Application.objects.get(student__pk=pk, course=course.pk).student

        return render(req, TEMPLETE_PATH % "adminnotification", locals())

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def sendnotificationmail(req):
        if req.is_ajax():
                enviar_notification(req.POST.get('subject'), req.POST.get('body'), req.POST.get('email'))

                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def adminhomework(req, slug):
        user = User.objects.get(username=req.user.username)
        teacher = TeacherPersonalInformation.objects.get(user=user.pk)
        subject = SubjectInformation.objects.filter(slug=slug).first()

        try:
                homeworks = HomeWork.objects.filter(
                        edition__active=True, 
                        clase__subject__slug=slug).order_by('-datepub')
                paginador = Paginator(homeworks, 25)

                page_number = req.GET.get('page')
                page_obj = paginador.get_page(page_number)

                del homeworks
        except:
                messages.error("No hay tareas para mostrar")

        return render(req, TEMPLETE_PATH % "adminhomeworks", locals())

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def apiadminhomework(req):
        if req.is_ajax():
                hw = HomeWork.objects.get(pk=req.POST.get('hw'))
                hw.note = req.POST.get('note')
                hw.save()

                return JsonResponse({'response': True})
        else:
                return HttpResponseForbidden()

@user_passes_test(isTeacher, login_url="/login/", redirect_field_name="next")
@login_required(login_url="/login/", redirect_field_name="next")
def registro(req, slug):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=registro-%s.csv' % slug

        # Creamos un escritor CSV usando a HttpResponse como "fichero"
        writer = csv.writer(response)
        writer.writerow(["Nombre", "Apellidos", "Nota"])
        for enrollment in Enrollment.objects.filter(subject__slug=slug):
                print(enrollment)
                # Nombre, Apellidos
                writer.writerow([enrollment.student.name, enrollment.student.lastname, 2])

        return response