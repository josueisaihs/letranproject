from django.db import models
from django.contrib import admin
from django.urls import reverse

from Docencia.DatosPersonales.models import StudentPersonalInformation
from Docencia.Cursos.models import CourseInformation, Edition


class EnrollmentApplication(models.Model):
    course = models.ForeignKey("CourseInformation", on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name="Nombre", blank=False, null=False)    

    class Meta:
        verbose_name = "Aplicación - Matrícula"
        verbose_name_plural = "Aplicación - Matrículas"
        unique_together = [('course', 'name')]

    def __str__(self):
        return "%s %s" % (self.course, self.name)

    def get_absolute_url(self):
        """Return absolute url for Curso."""
        return reverse('EnrollmentApplication.views.details', args=[str(self.id)])


@admin.register(EnrollmentApplication)
class EnrollmentApplicationAdmin(admin.ModelAdmin):
    '''Admin View for EnrollmentApplication'''
    list_display = ('course', 'name')
    search_fields = ('course__name', 'course__sede__name', 'name')
    ordering = ('name', 'course__name')
# <> fin EnrollmentApplication

class AskApplication(models.Model):
    app = models.ForeignKey('EnrollmentApplication', verbose_name="Aplicación", 
        on_delete=models.CASCADE)
    askBody = models.CharField(max_length=150, verbose_name="Pregunta", null=False, blank=False)
    askType = models.CharField(max_length=2, verbose_name="Tipo", 
        choices=(
                ("t", "Texto"), 
                ("o", "Opciones"),
                ("r", "Radio Botón"),
                ("c", "Check Botón"),
                # ("ac", "Argumenta Respuesta Positiva (¿Cuál?)"),
                # ("ad", "Argumenta Respuesta Positiva (¿Dónde?)"),
                # ("ap", "Argumenta Respuesta Positiva (¿Por qué?)"),
                # ("aa", "Argumenta Respuesta Positiva (Año)"),
            ), 
            default="t"
        )
    order = models.PositiveIntegerField(verbose_name="Orden")

    textMin = models.PositiveIntegerField(default=20, 
    verbose_name="Cantidad Mínima de Caracteres en la Respuesta")
    textMax = models.PositiveIntegerField(default=200, 
        verbose_name="Cantidad Máxima de Caracteres Permitidos en la Respuesta")

    options = []

    def __str__(self):
        return "%s %s - %s (%s)" % (self.app, self.order, self.askBody, self.askType)

    class Meta:
        verbose_name = 'Aplicación - Pregunta'
        verbose_name_plural = 'Aplicación - Preguntas'
        unique_together = [('app', 'askBody')]

    def get_absolute_url(self):
        """Return absolute url for Curso."""
        return reverse('AskApplication.views.details', args=[str(self.id)])

@admin.register(AskApplication)
class AskApplicationAdmin(admin.ModelAdmin):
    list_display = ('app', 'askBody', 'askType', 'order', 'textMin', 'textMax')
    fields = list_display   
    search_fields = ['app__name', 'app__course__name', 'askBody']
    list_filter = ["askType",]

# <> fin AskApplication


class OptionAskApplication(models.Model):
    askApp = models.ForeignKey('AskApplication', verbose_name="Pregunta", on_delete=models.CASCADE)
    option = models.CharField(max_length=250, blank=False, verbose_name="Opción")
    ispositive = models.BooleanField(default=False, verbose_name="¿Es Respuesta Positiva?")

    def __str__(self):
        return "%s %s" % (self.askApp, self.option)

    class Meta:
        unique_together = [('askApp', 'option')]
        verbose_name = 'Aplicación - Opción'
        verbose_name_plural = 'Aplicación - Opciones'
    
    def get_absolute_url(self):
        """Return absolute url for Curso."""
        return reverse('OptionAskApplication.views.details', args=[str(self.id)])

@admin.register(OptionAskApplication)
class OptionAskApplicationAdmin(admin.ModelAdmin):
    list_display = ('askApp', 'option', 'ispositive')
    fields = list_display
    search_fields = ['askApp__askBody', 'option', 'askApp__app__course__name']
# <> OptionAskApplication


class AnswerApplication(models.Model):
    askApp = models.ForeignKey('AskApplication', verbose_name="Pregunta", on_delete=models.CASCADE)
    student = models.ForeignKey('StudentPersonalInformation', verbose_name="Aspirante", 
        on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000, blank=False, verbose_name="Respuesta")
    appdate = models.DateField(verbose_name="Fecha Aplicación", auto_now=True, blank=False, 
        editable=False)

    def __str__(self):
        return "%s %s" % (self.askApp, self.student)

    class Meta:
        unique_together = [('askApp', 'student')]
        verbose_name = 'Aplicación - Respuesta'
        verbose_name_plural = 'Aplicación - Respuestas'
    
    def get_absolute_url(self):
        """Return absolute url for Curso."""
        return reverse('AnswerApplication.views.details', args=[str(self.id)])

@admin.register(AnswerApplication)
class AnswerApplicationAdmin(admin.ModelAdmin):
    list_display = ('askApp', 'student', 'answer', 'appdate')
    fields = list_display
    readonly_fields = ('appdate',)
    search_fields = ['askApp__askBody', 'askApp__app__course__name', 'askApp__app__name', 'student__name', 'student__lastname']
# <> fin AnswerApplication


class Application(models.Model):
    """Model definition for Application del Estudiante."""
    course = models.ForeignKey('CourseInformation', verbose_name="Curso", 
        on_delete=models.CASCADE)
    edition = models.ForeignKey('Edition', verbose_name='Edición', on_delete=models.CASCADE)
    student = models.ForeignKey('StudentPersonalInformation', verbose_name="Aspirante", 
        on_delete=models.CASCADE)
    appdate = models.DateField(verbose_name="Fecha Aplicación", auto_now=True, blank=False, 
        editable=False)

    status = models.CharField(
        max_length=9, 
        choices=(                
                ("espera", "En espera"), 
                ("proceso", "En proceso"),
                ("reserva", "En reserva"),
                ("aceptado", "Aceptado"), 
                ("denegado", "Denegado"),
            ), 
        default="espera"
    )
    comments = models.TextField(verbose_name='Comentarios', default="", blank=True)

    answers = []

    class Meta:
        """Meta definition for Application."""
        unique_together = [('course', 'student', 'edition')]
        verbose_name = 'Aplicación - Aplicación Estudiante'
        verbose_name_plural = 'Aplicación - Aplicaciones Estudiante'

    def __str__(self):
        """Unicode representation of Application."""
        return "%s %s %s" % (self.course, self.edition, self.student)

    def get_absolute_url(self):
        """Return absolute url for Application."""
        return reverse('Application.views.details', args=[str(self.id)])
    
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('course', 'edition', 'student', 'appdate', 'status')
    fields = list_display
    list_filter = ["edition", "status"]
    search_fields = ['course__name', 'edition__name', 'student__name', 'student__lastname']
    readonly_fields = ('appdate', 'comments')
# <> fin Application
