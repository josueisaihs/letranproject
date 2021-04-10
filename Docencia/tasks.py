from background_task import background

from django.core.mail import EmailMessage, BadHeaderError, send_mass_mail
from smtplib import SMTPException
from django.contrib.auth.models import User

from Docencia.Index.models import Suscriptor, RedesSociales
from Docencia.Cursos.models import Edition, CourseInformation
from Docencia.Admision.models import Application
from Docencia.DatosPersonales.models import StudentPersonalInformation

from validate_email import validate_email
import tweepy
import facebook

import logging
logger = logging.getLogger(__name__)

@background(schedule=10)
def notify_user(user_id):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user('Here is a notification', 'You have been notified')

@background(schedule=5)
def verificar_email(_email_):
    try:
        email = EmailMessage(
                "Centro Fray Bartolomé de las Casas", 
                "Se ha suscrito en el Centro Fray Bartolomé de las Casas.",
                to=[_email_],
        )
        if validate_email(_email_, verify=True):
            logger.info("Suscrito: <%s>" % _email_)
            email.send(fail_silently=False)
        else:
            suscriptor = Suscriptor.objects.get(email=_email_)
            suscriptor.delete()
            logger.warning("El email <%s>" % _email_)
    except TimeoutError as e:
        logger.exception("Error: TimeoutError %s" % _email_)

@background(schedule=5)
def enviar_suscriptores(slug, title:str, resumen:str, date:str):
    correos = []
    for suscriptor in Suscriptor.objects.all().only('email'):
        correos.append(suscriptor.email)
    cuerpo = """
        <html>
            <head>
            </head>
            <body style="width: 75%; margin: auto; padding: 5%;">        
                <div class="grid-container"> 
                    <div><h1 style="text-align: center; color: #660616;">¡Nueva Noticia!</h1></div>           
                    <div style="text-align: right;">
                        <a href='https://bartolo.org/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                            <img src="https://bartolo.org/static/img/cfbc.png" alt="Centro Fray Bartolomé de las Casas" height="50vh" />
                        </a>
                    </div>
                </div>
                <div style="border: #e6e2e2 solid 1px; padding: 2% 4%; border-radius: 15px;">
                    <h3>{}</h3>
                    <small>{}</small>        
                    <p>{}...
                    </p>
                    <a style="background-color: #660616; color: white; text-decoration: none; border: #660616 solid 1px; padding: 1% 2%; border-radius: 15px;" role="button" href='https://bartolo.org/noticia/{}/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                        Continua Leyendo ...
                    </a>
                </div>
                <br>
                <div style="text-align: center;"><small>Síguenos en Nuestras Redes Sociales</small></div>
                <div style="display: grid; grid-template-columns: auto auto auto; grid-gap: 10px; padding: 5%;">
                    <div style="text-align: center;"><a href="https://bit.ly/3dD0mGy">Facebook</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3fAINsK">Twitter</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3ewUEXl">YouTube</a></div>
                </div>       

                <p style="color:#555555; text-align: center;">Centro Fray Bartolomé de las Casas | 1998-2020</p>
            </body>
        </html>
    """.format(title, date, resumen, slug)
    email = EmailMessage(
                "Nueva Noticia · Centro Fray Bartolomé de las Casas", 
                cuerpo,
                bcc=correos,
    )
    email.content_subtype = "html" 
    email.send(fail_silently=True)

@background(schedule=5)
def twittertweet(slug, title, resumen, seccion="noticia"):
    tokens = RedesSociales.objects.get(active=True)
    
    auth = tweepy.OAuthHandler(tokens.consumer_key, tokens.consumer_secret)
    auth.set_access_token(tokens.access_token, tokens.access_token_secret)
    api = tweepy.API(auth)
    api.update_status("%s\n%s...\n%s\n#cfbc" % (title, resumen, "https://bartolo.org/%s/%s/?utm_source=twitter-tweet&utm_medium=twitter&utm_campaign=crecimiento" % (seccion, slug)))

@background(schedule=5)
def facebookposts(slug, title, resumen, seccion="noticia"):
    if tokens.facebook_token.__len__() > 0:
        tokens = RedesSociales.objects.get(active=True)
        graph = facebook.GraphAPI(access_token=tokens.facebook_token, version="2.8")
        graph.put_object(
            parent_object=tokens.facebook_id, 
            connection_name='feed',
            message="%s\n%s...\nLeer más" % (title, resumen),
            link="https://bartolo.org/%s/%s/?utm_source=facebook-posts&utm_medium=facebook&utm_campaign=crecimiento" % (seccion, slug)
        )

@background(schedule=5)
def enviar_evento_suscriptores(pk, title, resumen):
    correos = []
    for suscriptor in Suscriptor.objects.all().only('email'):
        correos.append(suscriptor.email)
    cuerpo = """
        <html>
            <head>
            </head>
            <body style="width: 75%; margin: auto; padding: 5%;">        
                <div class="grid-container"> 
                    <div><h1 style="text-align: center; color: #660616;">¡Nuevo Evento!</h1></div>           
                    <div style="text-align: right;">
                        <a href='https://bartolo.org/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                            <img src="https://bartolo.org/static/img/cfbc.png" alt="Centro Fray Bartolomé de las Casas" height="50vh" />
                        </a>
                    </div>
                </div>
                <div style="border: #e6e2e2 solid 1px; padding: 2% 4%; border-radius: 15px;">
                    <h3>{}</h3>        
                    <p>{}...
                    </p>
                    <a style="background-color: #660616; color: white; text-decoration: none; border: #660616 solid 1px; padding: 1% 2%; border-radius: 15px;" role="button" href='https://bartolo.org/evento/{}/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                        Más detalles ...
                    </a>
                </div>
                <br>
                <div style="text-align: center;"><small>Síguenos en Nuestras Redes Sociales</small></div>
                <div style="display: grid; grid-template-columns: auto auto auto; grid-gap: 10px; padding: 5%;">
                    <div style="text-align: center;"><a href="https://bit.ly/3dD0mGy">Facebook</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3fAINsK">Twitter</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3ewUEXl">YouTube</a></div>
                </div>       

                <p style="color:#555555; text-align: center;">Centro Fray Bartolomé de las Casas &copy; 1998-2020</p>
            </body>
        </html>
    """.format(title, resumen, pk)
    email = EmailMessage(
                "Nuevo Evento · Centro Fray Bartolomé de las Casas", 
                cuerpo,
                bcc=correos,
    )
    email.content_subtype = "html" 
    email.send(fail_silently=True)

@background(schedule=10)
def enviar_admitidos(edition_pk):
    # lookup user by id and send them a message
    edition = Edition.objects.get(pk=edition_pk)

    apps = Application.objects.filter(edition=edition, status="aceptado")
    for app in apps:
        student = StudentPersonalInformation.objects.get(pk=app.student.pk)
        email = EmailMessage(
                    "Admitido en el Centro Fray Bartolomé de las Casas", 
                    "Al recibir este correo electrónico, tenemos el placer de informarle que ha sido admitido para cursar el %s de %s. Para iniciar sus actividades chequée el CAMPUS VIRTUAL: https://bartolo.org/plataforma/dashboard/" % (app.course.category.name, app.course.name),
                    to=[student.email],
        )
        email.send(fail_silently=False)
   
@background(schedule=10)
def enviar_comunicado(edition_pk, course_pk, subject, body):
    apps = Application.objects.filter(
        edition=Edition.objects.get(pk=edition_pk), 
        course=CourseInformation.objects.get(pk=course_pk),
        status="aceptado"
    )

    email = EmailMessage(
        "CAMPUS VIRTUAL. %s" % subject,
        body + "\n\nNo conteste este correo electrónico",
        to=["centrofbc@gmail.com"]
    )
    email.send(fail_silently=False)

    for app in apps:
        email = EmailMessage(
            "CAMPUS VIRTUAL. %s" % subject,
            body + "\n\nNo conteste este correo electrónico",
            to=[app.student.email]
        )
        email.send(fail_silently=False)

@background(schedule=10)
def enviar_notification(subject, body, studentMail):
    email = EmailMessage(
        "CAMPUS VIRTUAL. %s" % subject,
        "%s\n\nNo conteste este correo electrónico" % body,
        bcc=["desarrollo@bartolo.org", "centrofbc@bartolo.org", studentMail]
    )
    email.send(fail_silently=False)

@background(schedule=10)
def enviar_admin(subject, body):
    email = EmailMessage(
        "CAMPUS VIRTUAL. PAGO",
        "%s" % body ,
        to=["desarrollo@bartolo.org",]
    )
    email.send(fail_silently=False)