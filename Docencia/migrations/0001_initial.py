# Generated by Django 3.1 on 2020-08-29 00:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Descripcion')),
                ('typeOf', models.BooleanField(default=True, verbose_name='¿Es docente?')),
            ],
            options={
                'verbose_name': 'Área',
                'verbose_name_plural': 'Curso - Áreas',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, unique=True, verbose_name='Autor')),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/image/comment', verbose_name='Foto Perfil')),
                ('body', models.TextField(max_length=1000, verbose_name='Comentario')),
            ],
            options={
                'verbose_name': 'Index - Comentario',
                'verbose_name_plural': 'Index - Comentario',
            },
        ),
        migrations.CreateModel(
            name='CourseInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='image/perfil/course')),
                ('capacity', models.PositiveSmallIntegerField(default=12, verbose_name='Capacidad')),
                ('openregistre', models.DateField(blank=True, verbose_name='Inicio Admisión')),
                ('deadline', models.DateField(blank=True, verbose_name='Fin Admisión')),
                ('description', models.TextField(blank=True, max_length=5000, verbose_name='Descripión')),
                ('price', models.PositiveSmallIntegerField(default=20, verbose_name='Precio')),
                ('curriculum', models.TextField(blank=True, max_length=5000, verbose_name='Curriculum')),
                ('requirements', models.TextField(blank=True, max_length=5000, verbose_name='Requisitos')),
                ('haveApplication', models.BooleanField(default=False, verbose_name='¿Tiene Formulario de Aplicación?')),
                ('yearMin', models.PositiveSmallIntegerField(default=18, verbose_name='Edad Minima')),
                ('yearMax', models.PositiveSmallIntegerField(default=40, verbose_name='Edad Máxima')),
                ('isService', models.BooleanField(default=False, verbose_name='¿Es un servicio?')),
                ('programa', models.FileField(blank=True, null=True, upload_to='media/static/cursos/programas', verbose_name='Programa')),
                ('reglamento', models.FileField(blank=True, null=True, upload_to='static/cursos/programas', verbose_name='Reglamento')),
                ('starts', models.SmallIntegerField(default=4, verbose_name='Puntuación')),
            ],
            options={
                'verbose_name': 'Curso / Servicio',
                'verbose_name_plural': 'Curso - Cursos y Servicios',
            },
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Aug 2020-Aug 2021', max_length=17, unique=True, verbose_name='Curso - Edición')),
                ('dateinit', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha de Inicio')),
                ('dateend', models.DateField(default=datetime.date(2021, 2, 25), verbose_name='Fecha de Fin')),
            ],
            options={
                'verbose_name': 'Curso - Edición',
                'verbose_name_plural': 'Curso - Ediciones',
            },
        ),
        migrations.CreateModel(
            name='HeaderIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('background', models.ImageField(blank=True, null=True, upload_to='static/image/index/bg', verbose_name='Background Image')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='static/image/index/icon', verbose_name='Icon')),
                ('titleLine1', models.CharField(max_length=20, verbose_name='Título Línea 1')),
                ('titleLine2', models.CharField(blank=True, max_length=20, verbose_name='Título Línea 2')),
                ('titleLine3', models.CharField(blank=True, max_length=20, verbose_name='Título Línea 3')),
                ('subtitle', models.CharField(blank=True, max_length=32, verbose_name='Subtítulo')),
                ('hadBtn1', models.BooleanField(default=False, verbose_name='Añadir Botón 1')),
                ('btn1', models.CharField(blank=True, max_length=10, verbose_name='Botón 1 Texto')),
                ('linkBtn1', models.CharField(blank=True, max_length=25, verbose_name='Botón 1 Enlace')),
                ('hadBtn2', models.BooleanField(default=False, verbose_name='Añadir Botón 2')),
                ('btn2', models.CharField(blank=True, max_length=10, verbose_name='Botón 2 Texto')),
                ('linkBtn2', models.CharField(blank=True, max_length=25, verbose_name='Botón 2 Enlace')),
                ('isVisible', models.BooleanField(default=False, verbose_name='Visible')),
            ],
            options={
                'verbose_name': 'Index - Header',
                'verbose_name_plural': 'Index - Header',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('section', models.CharField(choices=[('enl', 'Enlaces Útiles'), ('opr', 'Orden Predicadores')], default='enl', max_length=3, verbose_name='Sección')),
                ('link', models.URLField(verbose_name='Enlace')),
            ],
            options={
                'verbose_name': 'Index - Link',
                'verbose_name_plural': 'Index - Links',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Título')),
                ('body', models.TextField(verbose_name='Cuerpo')),
                ('link', models.URLField(blank=True, verbose_name='Enlace')),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/image/news')),
                ('date', models.DateTimeField(verbose_name='Fecha de Publicación')),
            ],
            options={
                'verbose_name': 'Index - Noticia',
                'verbose_name_plural': 'Index - Noticias',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Título')),
                ('body', models.TextField(verbose_name='Cuerpo')),
                ('link', models.URLField(blank=True, verbose_name='Enlace')),
                ('autor', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/image/blog')),
                ('date', models.DateTimeField(verbose_name='Fecha de Publicación')),
            ],
            options={
                'verbose_name': 'Index - Blog Post',
                'verbose_name_plural': 'Index - Blog Posts',
            },
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('recurso', models.FileField(blank=True, null=True, upload_to='static/recurso', verbose_name='Recurso')),
                ('tipo', models.CharField(choices=[('imagen', 'Imagen'), ('documento', 'Documento'), ('video', 'Video')], max_length=20, verbose_name='Tipo')),
                ('uploaddate', models.DateField(auto_now=True, verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'Recurso',
                'verbose_name_plural': 'Index - Recursos',
            },
        ),
        migrations.CreateModel(
            name='RespuestasError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(default='Yo', max_length=100, verbose_name='Autor')),
                ('body', models.CharField(max_length=300, verbose_name='Texto')),
            ],
            options={
                'verbose_name': 'Respuesta a Error',
                'verbose_name_plural': 'Index - Respuestas a Error',
            },
        ),
        migrations.CreateModel(
            name='SectionComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Nombre')),
                ('background', models.ImageField(blank=True, null=True, upload_to='static/image/index/bg', verbose_name='Background Image')),
            ],
            options={
                'verbose_name': 'Index - Sección Comentario',
                'verbose_name_plural': 'Index - Sección Comentarios',
            },
        ),
        migrations.CreateModel(
            name='SectionSuscribete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Sección Suscribete')),
                ('students', models.PositiveSmallIntegerField(default=0, verbose_name='Cantidad de Estudiantes [mil]')),
                ('graduados', models.PositiveIntegerField(default=0, verbose_name='Cantidad de Graduados [mil]')),
                ('cursos', models.PositiveIntegerField(default=0, verbose_name='Cantidad Cursos')),
                ('background', models.ImageField(blank=True, null=True, upload_to='static/image/index/bg', verbose_name='Background Image')),
            ],
            options={
                'verbose_name': 'Index - Sección Suscríbete',
                'verbose_name_plural': 'Index - Sección Suscríbete',
            },
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Nombre')),
                ('openhor', models.TimeField(verbose_name='Apertura')),
                ('closehor', models.TimeField(verbose_name='Cierre')),
                ('isprincipal', models.BooleanField(default=False, verbose_name='¿Es la Sede Principal?')),
                ('street', models.CharField(blank=True, max_length=100, null=True, verbose_name='Calle')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='Municipio')),
                ('state', models.CharField(blank=True, max_length=50, null=True, verbose_name='Provincia')),
                ('cellphone', models.CharField(blank=True, max_length=8, null=True, verbose_name='Móvil')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('reglamento', models.FileField(blank=True, null=True, upload_to='static/sedes/reglamentos', verbose_name='Reglamento')),
            ],
            options={
                'verbose_name': 'Sede',
                'verbose_name_plural': 'Sedes',
            },
        ),
        migrations.CreateModel(
            name='Suscriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('ip', models.GenericIPAddressField(verbose_name='Dirección IP')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'Index - Subscriptor',
                'verbose_name_plural': 'Index - Subscriptores',
            },
        ),
        migrations.CreateModel(
            name='TeacherPersonalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('lastname', models.CharField(max_length=50, verbose_name='Apellido')),
                ('gender', models.CharField(choices=[('m', 'Masculino'), ('f', 'Femenino')], default='m', max_length=1, verbose_name='Género')),
                ('numberidentification', models.CharField(max_length=11, unique=True, verbose_name='Carnet de Identidad')),
                ('street', models.CharField(max_length=100, verbose_name='Calle')),
                ('city', models.CharField(max_length=50, verbose_name='Municipio')),
                ('state', models.CharField(max_length=50, verbose_name='Provincia')),
                ('cellphone', models.CharField(blank=True, max_length=8, null=True, verbose_name='Móvil')),
                ('phone', models.CharField(blank=True, max_length=8, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('nacionality', models.CharField(default='cubana', max_length=50, verbose_name='Nacionalidad')),
                ('pasaport', models.CharField(blank=True, max_length=10, null=True, verbose_name='Pasaporte')),
                ('degree', models.CharField(choices=[('Ing.', 'Ingeniero'), ('Arq.', 'Arquitecto'), ('Lic.', 'Licenciado'), ('Ms.C.', 'Master en Ciencias'), ('Dr.C.', 'Doctor en Ciencias'), ('PhD.C.', 'Postdoctor en Ciencias'), ('Otro', 'Otro'), ('Ning.', 'Ninguno')], default='Lic.', max_length=20, verbose_name='Grado Científico')),
                ('title', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Título')),
                ('dateinit', models.DateField(blank=True, null=True, verbose_name='Fecha de Inicio')),
                ('dateend', models.DateField(blank=True, null=True, verbose_name='Fecha de Fin')),
                ('user', models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Datos Personales - Profesor',
                'verbose_name_plural': 'Datos Personales - Profesores',
                'unique_together': {('name', 'lastname', 'numberidentification', 'email')},
            },
        ),
        migrations.CreateModel(
            name='StudentPersonalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre(s)')),
                ('lastname', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('gender', models.CharField(choices=[('m', 'Masculino'), ('f', 'Femenino'), ('n', 'No Declaro')], default='m', max_length=1, verbose_name='Género')),
                ('numberidentification', models.CharField(max_length=11, unique=True, verbose_name='Número de Identificación')),
                ('nacionality', models.CharField(default='cubana', max_length=50, verbose_name='Nacionalidad')),
                ('street', models.CharField(max_length=100, verbose_name='Calle')),
                ('city', models.CharField(max_length=50, verbose_name='Municipio / Ciudad')),
                ('state', models.CharField(max_length=50, verbose_name='Provincia / Estado')),
                ('cellphone', models.CharField(blank=True, max_length=8, null=True, verbose_name='Móvil')),
                ('phone', models.CharField(blank=True, max_length=8, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Eletrónico')),
                ('degree', models.CharField(choices=[('Ing.', 'Ingeniero'), ('Arq.', 'Arquitecto'), ('Lic.', 'Licenciado'), ('Ms.C.', 'Master en Ciencias'), ('Dr.C.', 'Doctor en Ciencias'), ('PhD.C.', 'Postdoctor en Ciencias'), ('Otro', 'Otro'), ('Ning.', 'Ninguno')], default='Ning.', max_length=20, verbose_name='Grado Científico')),
                ('title', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Título')),
                ('ocupation', models.CharField(choices=[('te', 'Trabajador Estatal'), ('ac', 'Ama/o de Casa'), ('tp', 'Trabajador Privado'), ('do', 'Desocupado'), ('es', 'Estudiante')], default='do', max_length=2, verbose_name='Ocupación')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Estudiante o Aspirante',
                'verbose_name_plural': 'Datos Personales - Estudiantes / Aspirantes',
                'unique_together': {('name', 'lastname', 'numberidentification', 'email')},
            },
        ),
        migrations.CreateModel(
            name='EventsDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateEnv', models.DateTimeField(verbose_name='Fecha Inicio')),
                ('dateFin', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha Fin')),
            ],
            options={
                'verbose_name': 'Index - Evento Fecha',
                'verbose_name_plural': 'Index - Eventos Fechas',
                'unique_together': {('dateEnv', 'dateFin')},
            },
        ),
        migrations.CreateModel(
            name='EnrollmentApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nombre')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.courseinformation')),
            ],
            options={
                'verbose_name': 'Aplicación - Matrícula',
                'verbose_name_plural': 'Aplicación - Matrículas',
                'unique_together': {('course', 'name')},
            },
        ),
        migrations.CreateModel(
            name='CourseSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('Lun.', 'Lunes'), ('Mar.', 'Martes'), ('Mié.', 'Miércoles'), ('Jue.', 'Jueves'), ('Vie.', 'Viernes'), ('Sáb.', 'Sábado'), ('Lun.-Vie.', 'Lunes a Viernes'), ('Lun.-Sáb.', 'Lunes a Sábado'), ('Lun.,Mié.,Vie.', 'Lunes, Miércoles, Viernes'), ('Mar.,Jue.', 'Martes, Jueves')], default='Lun.', max_length=14)),
                ('dateIni', models.TimeField(verbose_name='Fecha Inicio')),
                ('dateFin', models.TimeField(default=django.utils.timezone.now, verbose_name='Fecha Fin')),
            ],
            options={
                'verbose_name': 'Horario',
                'verbose_name_plural': 'Cursos - Horarios',
                'unique_together': {('weekday', 'dateIni', 'dateFin')},
            },
        ),
        migrations.AddField(
            model_name='courseinformation',
            name='adminteachers',
            field=models.ManyToManyField(related_name='teachers', related_query_name='teacher_admin', to='Docencia.TeacherPersonalInformation', verbose_name='Profesores Encargados'),
        ),
        migrations.AddField(
            model_name='courseinformation',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.area', verbose_name='Area'),
        ),
        migrations.AddField(
            model_name='courseinformation',
            name='schedules',
            field=models.ManyToManyField(blank=True, to='Docencia.CourseSchedule', verbose_name='Horario(s)'),
        ),
        migrations.AddField(
            model_name='courseinformation',
            name='sedes',
            field=models.ManyToManyField(related_name='sedes', related_query_name='sedes', to='Docencia.Sede', verbose_name='Sede(s)'),
        ),
        migrations.CreateModel(
            name='Colaboradores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('lastname', models.CharField(max_length=50, verbose_name='Apellido')),
                ('gender', models.CharField(choices=[('m', 'Masculino'), ('f', 'Femenino')], default='m', max_length=1, verbose_name='Género')),
                ('numberidentification', models.CharField(max_length=11, unique=True, verbose_name='Carnet de Identidad')),
                ('street', models.CharField(max_length=100, verbose_name='Calle')),
                ('city', models.CharField(max_length=50, verbose_name='Municipio')),
                ('state', models.CharField(max_length=50, verbose_name='Provincia')),
                ('cellphone', models.CharField(blank=True, max_length=8, null=True, verbose_name='Móvil')),
                ('phone', models.CharField(blank=True, max_length=8, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('labor', models.TextField(max_length=1000, verbose_name='Labor')),
                ('dateinit', models.DateField(blank=True, null=True, verbose_name='Fecha de Inicio')),
                ('dateend', models.DateField(blank=True, null=True, verbose_name='Fecha de Fin')),
                ('curriculum', models.FileField(blank=True, null=True, upload_to='static/curriculum/colaborador', verbose_name='Curriculum')),
            ],
            options={
                'verbose_name': 'Datos Personales - Colaborador',
                'verbose_name_plural': 'Datos Personales - Colaboradores',
                'unique_together': {('name', 'lastname', 'numberidentification', 'email')},
            },
        ),
        migrations.CreateModel(
            name='AskApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('askBody', models.CharField(max_length=150, verbose_name='Pregunta')),
                ('askType', models.CharField(choices=[('t', 'Texto'), ('o', 'Opciones'), ('r', 'Radio Botón'), ('c', 'Check Botón')], default='t', max_length=2, verbose_name='Tipo')),
                ('order', models.PositiveIntegerField(verbose_name='Orden')),
                ('textMin', models.PositiveIntegerField(default=20, verbose_name='Cantidad Mínima de Caracteres en la Respuesta')),
                ('textMax', models.PositiveIntegerField(default=200, verbose_name='Cantidad Máxima de Caracteres Permitidos en la Respuesta')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.enrollmentapplication', verbose_name='Aplicación')),
            ],
            options={
                'verbose_name': 'Aplicación - Pregunta',
                'verbose_name_plural': 'Aplicación - Preguntas',
                'unique_together': {('app', 'askBody')},
            },
        ),
        migrations.CreateModel(
            name='OptionAskApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=250, verbose_name='Opción')),
                ('ispositive', models.BooleanField(default=False, verbose_name='¿Es Respuesta Positiva?')),
                ('askApp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.askapplication', verbose_name='Pregunta')),
            ],
            options={
                'verbose_name': 'Aplicación - Opción',
                'verbose_name_plural': 'Aplicación - Opciones',
                'unique_together': {('askApp', 'option')},
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('body', models.TextField(max_length=1000, verbose_name='Descripción')),
                ('date', models.DateTimeField(verbose_name='Fecha Publicación')),
                ('place', models.CharField(max_length=500, verbose_name='Lugar')),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/event/image')),
                ('file', models.FileField(blank=True, null=True, upload_to='static/event/file')),
                ('google_maps', models.TextField(blank=True, max_length=1000, verbose_name='Embeber Google Maps')),
                ('dateEnvs', models.ManyToManyField(to='Docencia.EventsDate', verbose_name='Fecha(s)')),
                ('user', models.ForeignKey(default=1, limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Index - Eventos',
                'unique_together': {('name', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appdate', models.DateField(auto_now=True, verbose_name='Fecha Aplicación')),
                ('status', models.CharField(choices=[('espera', 'En espera'), ('proceso', 'En proceso'), ('reserva', 'En reserva'), ('aceptado', 'Aceptado'), ('denegado', 'Denegado')], default='espera', max_length=9)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.courseinformation', verbose_name='Curso')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.edition', verbose_name='Edición')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.studentpersonalinformation', verbose_name='Aspirante')),
            ],
            options={
                'verbose_name': 'Aplicación - Aplicación Estudiante',
                'verbose_name_plural': 'Aplicación - Aplicaciones Estudiante',
                'unique_together': {('course', 'student', 'edition')},
            },
        ),
        migrations.CreateModel(
            name='AnswerApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1000, verbose_name='Respuesta')),
                ('appdate', models.DateField(auto_now=True, verbose_name='Fecha Aplicación')),
                ('askApp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.askapplication', verbose_name='Pregunta')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Docencia.studentpersonalinformation', verbose_name='Aspirante')),
            ],
            options={
                'verbose_name': 'Aplicación - Respuesta',
                'verbose_name_plural': 'Aplicación - Respuestas',
                'unique_together': {('askApp', 'student')},
            },
        ),
    ]
