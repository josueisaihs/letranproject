from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib import admin
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Docencia.validators import valid_extension, valid_size


class Class(models.Model):
    """Model definition for Class."""
    slug = models.SlugField(max_length=250, default="")
    subject = models.ForeignKey("Docencia.SubjectInformation", verbose_name="Asignatura", 
    on_delete=models.CASCADE, default=1)
    name = models.CharField(verbose_name="Nombre", max_length=100)
    classbody=CKEditor5Field('Cuerpo', config_name='extends')
    uploaddate = models.DateField('Fecha Creación', auto_now=True)
    datepub = models.DateTimeField('Fecha Pub.', auto_now=False, auto_now_add=False)
    resources =  models.ManyToManyField("Docencia.Recurso", verbose_name="Recursos", blank=True, limit_choices_to={'access': False})

    class Meta:
        """Meta definition for Class."""
        unique_together = ('subject', 'name')
        verbose_name = 'Clase'
        verbose_name_plural = 'Plataforma - Clases'

    def __str__(self):
        """Unicode representation of Class."""
        return "%s %s (%s)" % (self.subject, self.name, self.uploaddate)

    def slugConst(self):
        return "%s %s %s %s" % (self.subject.course.area.name, self.subject.course.name, self.subject.name, self.name)
    
    def _get_unique_slug(self):
        slug = slugify(self.slugConst())
        unique_slug = slug
        num = 1
        while Class.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    '''Admin View for Class'''
    list_display = ('subject', 'name', 'uploaddate', 'datepub')
    list_filter = ('subject__course', 'subject__course__area')
    search_fields = ('subject__course__name', 'subject__course__sede__name', 'subject__name', 'subject__course__area__name')
    ordering = ('-uploaddate',)
    readonly_fields = ('uploaddate', 'slug')

class HomeWork(models.Model):
    slug = models.SlugField("Slug", max_length=500)
    name = models.CharField("Nombre", max_length=250, default="Tarea 1")
    clase = models.ForeignKey("Docencia.Class", 
        verbose_name="Clase", 
        on_delete=models.CASCADE
    )
    student = models.ForeignKey("Docencia.StudentPersonalInformation", 
        verbose_name="Estudiante", 
        on_delete=models.CASCADE
    )
    file = models.FileField("Archivo", 
        upload_to='static/homework/%Y/%m/%d/%H/%M/', 
        max_length=1000,
        validators=[valid_extension, valid_size],
        help_text="Máximo tamaño de archivo permitido es 10MB"
    )
    datepub = models.DateTimeField("Fecha", auto_now=True)
    edition = models.ForeignKey("Docencia.Edition", verbose_name="Edición", on_delete=models.CASCADE, default=1)
    observations = models.TextField("Observaciones", default="")
    note = models.PositiveSmallIntegerField("Nota", default=2)

    class Meta:
        """Meta definition for MODELNAME."""
        unique_together = ('name', 'clase', 'student', 'edition')
        verbose_name = 'Docencia - Tarea'
        verbose_name_plural = 'Docencia - Tareas'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return "%s %s" % (self.clase, self.student)
    
    def _get_unique_slug(self):
        slug = slugify("%s %s %s %s %s" % (self.name, self.student.name, self.student.lastname, self.clase.subject.name, self.clase.name))
        unique_slug = slug
        num = 1
        while HomeWork.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    '''Admin View for HomeWork'''
    list_display = ('name', 'clase', 'student', 'datepub', 'file', 'edition', 'note')
    list_filter = ('clase__subject__course', 'clase__subject', 'edition')
    search_fields = ('name', 'clase__name', 'clase__subject__name', 'clase__subject__course__name', 'student__name', 'student__lastname')
    ordering = ('clase__name',)


class Message(models.Model):
    """Model definition for MODELNAME."""
    slug = models.SlugField(max_length=140, unique=True)
    edition = models.ForeignKey("Edition", verbose_name="Edition", on_delete=models.CASCADE, default=1)
    subject = models.ForeignKey("SubjectInformation", verbose_name="Asignatura", 
    on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE, default=1)
    # body = CKEditor5Field('Cuerpo', config_name='extends')
    body = models.CharField(verbose_name="Mensaje", max_length=180)
    audio = models.FileField("Audios", 
        upload_to='static/msg/audios/%Y/%m/%d/%H/%M/', 
        max_length=100, blank=True)
    typeMsg = models.CharField(
        "Tipo", 
        max_length=50, 
        choices=(
            ('Texto', 'Texto'), 
            ('Audio', 'Audio')
        ),
        default="Texto"
    )
    createdate = models.DateField('Fecha Creación', auto_now=True)
    approved = models.BooleanField("Aprobación", default=True)

    def approve(self):
        self.approved = True
        self.save()

    class Meta:
        """Meta definition for MODELNAME."""
        verbose_name = 'Mensajes'
        verbose_name_plural = 'Plataforma - Mensajes'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return "%s" % self.user.username

    def _get_unique_slug(self):
        slug = slugify("%s %s %s" % (self.subject.name, self.edition.name, self.user.username))
        unique_slug = slug
        num = 1
        while Message.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    '''Admin View for Message'''
    list_display = ('subject', 'user', 'createdate', 'approved', 'edition')
    list_filter = ('approved', 'subject__course__area', 'edition')
    search_fields = ('subject__name', 'user__name')
    ordering = ('-createdate',)


class Enrollment(models.Model):
    """Model definition for Enrollment."""
    slug = models.SlugField('Slug', default="", max_length=140)
    student = models.ForeignKey("Docencia.StudentPersonalInformation", verbose_name="Estudiante", 
    on_delete=models.CASCADE)
    subject = models.ForeignKey("Docencia.SubjectInformation", verbose_name="Asignatura", 
    on_delete=models.CASCADE)
    edition = models.ForeignKey("Docencia.Edition", verbose_name="Edition", 
    on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Estado", 
        choices=(
            ('Aprobado', 'Aprobado'),
            ('Suspenso', 'Suspenso'),
            ('En curso', 'En curso')
        ), max_length=8, default="En curso"
    )
    attempt = models.PositiveIntegerField(verbose_name="Intentos", default=1)
    
    # Cantidad de ausencias
    absence = models.PositiveSmallIntegerField(verbose_name="Inasistencias", default=0)

    # Notas
    nota = models.PositiveSmallIntegerField(verbose_name="Nota", default=2)

    def newAttempt(self):
        if self.attempt < 3:
            self.attempt = self.attempt + 1
            self.save()
        else:
            raise ValidationError('Ha alcanzado el máximo número de intentos')
    
    def newAbsence(self):
        if self.absence < 3:
            self.absence = self.absence + 1
            self.save()
        else:
            raise ValidationError('Ha alcanzado el máximo número de inasistencias')
    
    def setAbsence(self):
        if self.absence > 0:
            self.absence = self.absence - 1
            self.save()
        else:
            raise ValidationError('No tiene inasistencias')

    def getHomeWorks(self):
        return HomeWork.objects.filter(
            edition__active=True, 
            clase__subject__slug=self.subject.slug,
            student=self.student.pk
            ).order_by('-datepub')
    
    def getHWAverage(self):
        return 

    class Meta:
        """Meta definition for Enrollment."""
        unique_together = ('subject', 'student', 'edition')
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        """Unicode representation of Enrollment."""
        return "%s %s %s" % (self.student.fullname(), self.subject.name, self.edition.name)

    def _get_unique_slug(self):
        slug = slugify("%s" % (self.__str__()))
        unique_slug = slug
        num = 1
        while Enrollment.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    '''Admin View for Enrollment'''
    list_display = ('student', 'subject', 'edition', 'status', 'attempt', 'absence', "nota")
    list_filter = ('edition', 'status')
    search_fields = ('student__name', 'student__lastname', 'subject__name', 'subject__course__name')
    ordering = ('student', '-edition')
    readonly_fields = ('slug',)

class GroupInformation(models.Model):
    """Model definition for GroupInformation."""
    slug = models.SlugField('Slug', default="", max_length=200)
    name = models.CharField(verbose_name="Nombre", max_length=150)
    edition = models.ForeignKey('Docencia.Edition', verbose_name="Edición", on_delete=models.CASCADE)
    teachers = models.ManyToManyField('Docencia.TeacherPersonalInformation', verbose_name="Profesor(s)")
    enrollment = models.ManyToManyField('Docencia.Enrollment', verbose_name="Estudiante(s)", blank=True, limit_choices_to={'edition__active': True})

    class Meta:
        """Meta definition for GroupInformation."""
        unique_together = [('name', 'edition')]
        verbose_name = 'Grupo'
        verbose_name_plural = 'Cursos - Grupos'

    def _get_unique_slug(self):
        slug = slugify("%s %s %s" % (self.course.area.name, self.course.name, self.name))
        unique_slug = slug
        num = 1
        while GroupInformation.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of GroupInformation."""
        return "%s-%s %s" % (self.course, self.edition, self.name)

@admin.register(GroupInformation)
class GroupInformationAdmin(admin.ModelAdmin):
    '''Admin View for GroupInformation'''
    list_display = ('name', 'edition')
    list_filter = ('edition',)
    search_fields = ('name', 'edition__name', 'teachers__name', 'teachers__lastname',
    'students__name', 'students__lastname')
    ordering = ('name',)
    readonly_fields = ["slug",]
class Raspberry(models.Model):
    """Model definition for Raspberry."""
    name = models.CharField("Nombre", max_length=50, unique=True)
    slug = models.SlugField("Slug")

    class Meta:
        """Meta definition for Raspberry."""
        verbose_name = 'Raspberry'
        verbose_name_plural = 'Raspberrys'

    def __str__(self):
        """Unicode representation of Raspberry."""
        return self.name.__str__()

    def _get_unique_slug(self):
        slug = slugify("%s" % (self.name))
        unique_slug = slug
        num = 1
        while Raspberry.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(Raspberry)
class RaspberryAdmin(admin.ModelAdmin):
    '''Admin View for Raspberry'''
    list_display = ('name',)
    readonly_fields = ('slug',)
    search_fields = ('name',)
    ordering = ('name',)


class RoomClass(models.Model):
    """Model definition for RoomClass."""
    name = models.CharField('Nombre', max_length=50)
    raspberry = models.ForeignKey("Docencia.Raspberry", verbose_name='Raspberry', 
    on_delete=models.CASCADE)
    slug = models.SlugField('Slug')

    class Meta:
        """Meta definition for RoomClass."""
        unique_together = [('name', 'raspberry')]
        verbose_name = 'RoomClass'
        verbose_name_plural = 'RoomClasss'

    def __str__(self):
        """Unicode representation of RoomClass."""
        return self.name.__str__()

    def _get_unique_slug(self):
        slug = slugify("%s" % (self.name))
        unique_slug = slug
        num = 1
        while RoomClass.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

@admin.register(RoomClass)
class RoomClassAdmin(admin.ModelAdmin):
    '''Admin View for RoomClass'''
    list_display = ('name', 'raspberry')
    readonly_fields = ('slug',)
    search_fields = ('name', 'raspberry__name')
    ordering = ('name', 'raspberry__name')

class Assistence(models.Model):
    """Model definition for Assistence."""
    enrollment = models.ForeignKey("Docencia.Enrollment", verbose_name='Matrícula', 
    on_delete=models.CASCADE)
    roomclass = models.ForeignKey("Docencia.RoomClass", verbose_name='Aula', 
    on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=(
            ("a", "Asistencia"), 
            ("i", "Inasistencia"),
        ),
        default="a"
    )
    datepub = models.DateTimeField('Fecha', auto_now=True)

    class Meta:
        """Meta definition for Assistence."""
        unique_together = [('enrollment', 'roomclass', 'datepub')]
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        """Unicode representation of Assistence."""
        return "%s - %s - %s" % (self.enrollment.__str__(), self.roomclass.name, self.status)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

@admin.register(Assistence)
class AssistenceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'roomclass', 'status', 'datepub')
    list_filter = ('enrollment__subject__course__name', 'status')
    readonly_fields = ('datepub',)
    search_fields = ('enrollment__student__name', 'enrollment__student__lastname', 
    'enrollment__subject__name', 'enrollment__subject__course__name', 'roomclass__name', 
    'roomclass__raspberry__name')
    ordering = ('-datepub',)

class EnrollmentPay(models.Model):
    """Model definition for EnrollmentPay."""
    app = models.ForeignKey("Docencia.Application", verbose_name="Aplicacion", on_delete=models.CASCADE)
    transfernumber = models.CharField("Numero Transferencia", max_length=13, unique=True)
    accept = models.BooleanField(verbose_name="Aceptar Transferencia", default=False)

    class Meta:
        """Meta definition for EnrollmentPay ."""
        unique_together = [("app", "transfernumber")]
        verbose_name = 'Pago Matricula'
        verbose_name_plural = 'Pagos Matriculas'

    def __str__(self):
        """Unicode representation of EnrollmentPa."""
        return "%s %s" % (self.app.stundet, self.app.course)

    def save(self):
        """Save method for EnrollmentPay ."""
        pass

@admin.register(EnrollmentPay)
class EnrollmentPayAdmin(admin.ModelAdmin):
    '''Admin View for EnrollmentPay'''

    list_display = ('app', 'transfernumber', 'accept')
    list_filter = ('accept', 'app__course__area', 'app__course', 'app__edition')
    readonly_fields = ('transfernumber',)
    search_fields = ('app__student__name', 'app__student__lastname', 'app__course__name')
    ordering = ('app__student__lastname',)

class AccountNumber(models.Model):
    """Model definition for AccountNumber."""
    accountnumber = models.CharField("Numero de Cuenta", max_length=16, unique=True)
    owner = models.CharField("Propietario", max_length=50)

    class Meta:
        """Meta definition for AccountNumber."""
        unique_together = [('accountnumber', 'owner')]
        verbose_name = 'Numero de Cuenta'
        verbose_name_plural = 'Numeros de Cuentas'

    def __str__(self):
        """Unicode representation of AccountNumber."""
        return "%s %s" % (self.accountnumber, self.owner)

@admin.register(AccountNumber)
class AccountNumberAdmin(admin.ModelAdmin):
    '''Admin View for AccountNumber'''
    list_display = ('owner', 'accountnumber')
    search_fields = ('owner', 'accountnumber')
    ordering = ('owner',)
