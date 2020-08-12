from django.db import models, IntegrityError
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

def eliminarTildes(txt):
        w = (
            ("á", "a"), 
            ("é", "e"), 
            ("í", "i"), 
            ("ó", "o"), 
            ("ú", "u"),
            ("ñ", "n")
        )
        for x, y in w:
            txt = txt.replace(x, y)
        return txt

class StudentPersonalInformation(models.Model):
    """Model definition for StudentPersonalInformation. 
    Define a los estudiantes y los aspirantes que apliquen a una asignatura"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, verbose_name="Nombre(s)")
    lastname = models.CharField(max_length=50, verbose_name="Apellidos")

    gender = models.CharField(max_length=1, verbose_name="Género", choices=(("m", "Masculino"), ("f", "Femenino"), ("n", "No Declaro")), default="m")

    numberidentification = models.CharField(verbose_name="Número de Identificación", max_length=11, unique=True)

    nacionality = models.CharField(verbose_name="Nacionalidad", max_length=50, blank=False, null=False, default="cubana")

    street = models.CharField(verbose_name="Calle", max_length=100, null=False)
    city = models.CharField(verbose_name="Municipio / Ciudad", max_length=50, null=False)
    state = models.CharField(verbose_name="Provincia / Estado", max_length=50, null=False)

    cellphone = models.CharField(verbose_name="Móvil", max_length=8, blank=True, null=True)
    phone = models.CharField(verbose_name="Teléfono", max_length=8, blank=True, null=True)

    email = models.EmailField(verbose_name="Correo Eletrónico")

    degree = models.CharField(verbose_name="Grado Científico", max_length=20,
                              choices=(("Ing.", "Ingeniero"), ("Lic.", "Licenciado"), ("Ms.C.", "Master en Ciencias"),
                                       ("Dr.C.", "Doctor en Ciencias"), ("PhD.C.", "Postdoctor en Ciencias"),
                                       ("Ning.", "Ninguno")),
                              default="Ning.")
    title = models.CharField(verbose_name="Título", max_length=100, blank=True, null=True, default="")

    ocupation = models.CharField(max_length=2, verbose_name="Ocupación", 
                                 choices=(("te", "Trabajador Estatal"), ("ac", "Ama/o de Casa"),
                                          ("tp", "Trabajador Privado"), ("do", "Desocupado"), ("es", "Estudiante")),
                                 default="do")
    
    pwd = None

    class Meta:
        """Meta definition for StudentPersonalInformation."""
        unique_together = [('name', 'lastname', 'numberidentification', 'email')]
        verbose_name = 'Estudiante o Aspirante'
        verbose_name_plural = 'Datos Personales - Estudiantes / Aspirantes'

    def __str__(self):
        """Unicode representation of StudentPersonalInformation."""
        return "%s %s %s" % (self.degree, self.name, self.lastname)

    def get_absolute_url(self):
        """Return absolute url for StudentPersonalInformation."""
        return reverse('StudentPersonalInformation.views.details', args=[str(self.id)])

    def save(self):
        try:
            # Crea el usuario, en caso que exista da error
            self.user = self.createUser()
        except IntegrityError:
            pass
        super().save()

    def createUser(self):
        """ Crea un usuario con una contraseña cualquiera, despues se cambia"""

        pwd = "123456587";

        user = User.objects.create_user(
            username=self.email, 
            password=self.email,
            first_name=self.name,
            last_name=self.lastname,
            email=self.email
        )
        user.save()

        group = Group.objects.get(name='Estudiantes')
        user.groups.add(group)

        user = User.objects.get(
            username=self.email, 
            first_name=self.name,
            last_name=self.lastname
        )

        return user

    def fullname(self):
        return "%s %s" % (self.name, self.lastname)

    class Admin(ModelAdmin):
        fields = ["name", "lastname", "gender", "numberidentification", "street", "city", "state", "cellphone", "phone",
                  "email", "nacionality", "ocupation", "degree", "title"]
        ordering = ["numberidentification", "lastname", "name"]
        search_fields = fields
        list_display = fields


class TeacherPersonalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=2)

    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    gender = models.CharField(max_length=1, choices=(("m", "Masculino"), ("f", "Femenino")), default="m")

    numberidentification = models.CharField(max_length=11, unique=True)

    street = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)

    cellphone = models.CharField(max_length=8, blank=True, null=True)
    phone = models.CharField(max_length=8, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    nacionality = models.CharField(max_length=50, blank=False, null=False, default="cubana")
    pasaport = models.CharField(max_length=10, blank=True, null=True)

    degree = models.CharField(max_length=20,
                              choices=(("Ing.", "Ingeniero"), ("Lic.", "Licenciado"), ("Ms.C.", "Master en Ciencias"),
                                       ("Dr.C.", "Doctor en Ciencias"), ("PhD.C.", "Postdoctor en Ciencias"),
                                       ("Ning.", "Ninguno")),
                              default="Lic.")
    title = models.CharField(max_length=100, blank=True, null=True, default="")
    
    dateinit = models.DateField(blank=True, null=True, verbose_name="Fecha de Inicio")
    dateend = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin")

    class Meta:
        unique_together = [('name', 'lastname', 'numberidentification', 'email')]
        verbose_name = 'Datos Personales - Profesor'
        verbose_name_plural = 'Datos Personales - Profesores'

    def __str__(self):
        """Unicode representation of TeacherPersonalInformation."""
        return "%s %s %s" % (self.degree, self.name, self.lastname)

    def get_absolute_url(self):
        """Return absolute url for StudentPersonalInformation."""
        return reverse('TeacherPersonalInformation.views.details', args=[str(self.id)])

    # def save(self):
    #     try:
    #         # Crea el usuario, en caso que exista da error
    #         self.user = self.createUser()
    #     except ValueError:
    #         pass
    #     except IntegrityError:
    #         pass
    #     super().save()

    def createUser(self):
        """ Crea un usuario con una contraseña cualquiera, despues se cambia"""

        pwd ="%s" % self.email;

        user = User.objects.create_user(
            username=self.email, 
            password=self.email,
            first_name=self.name,
            last_name=self.lastname,
            email=self.email
        )
        user.save()

        group = Group.objects.get(name='Profesores')
        user.groups.add(group)

        user = User.objects.get(
            username=self.email, 
            first_name=self.name,
            last_name=self.lastname
        )

        return user

    class Admin(ModelAdmin):
        fields = ["user", "name", "lastname", "gender", "numberidentification", "street", "city", "state", "cellphone", "phone",
                  "email", "nacionality", "pasaport", "dateinit", "dateend"]
        ordering = ["numberidentification", "lastname", "name"]
        search_fields = fields
        list_display = fields