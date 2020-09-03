from background_task import background

from django.core.mail import EmailMessage, BadHeaderError, send_mass_mail
from smtplib import SMTPException
from django.contrib.auth.models import User

from Docencia.Index.models import Suscriptor

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
def enviar_suscriptores(pk:int, title:str, resumen:str, date:str):
    correos = []
    for suscriptor in Suscriptor.objects.all().only('email'):
        correos.append(suscriptor.email)
    cuerpo = """
        <html>
            <head>
                <style>
                    body {
                        width: 75%;
                        margin: auto;
                        padding: 5%;
                    }
                    h1 {
                        text-align: center;
                        color: #660616;
                    }
                    .grid-container {
                        display: grid;
                        grid-template-columns: auto auto auto;
                        grid-gap: 10px;
                        padding: 5%;
                    }
                </style>
            </head>
            <body>        
                <div class="grid-container"> 
                    <div><h1>¡Nueva Noticia!</h1></div>           
                    <div style="text-align: right;">
                        <a href='https://bartolo.org/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                            <img src="https://bartolo.org/static/img/cfbc.png" alt="Centro Fray Bartolomé de las Casas" height="50vh" />
                        </a>
                    </div>
                </div>
                <div style="border: #e6e2e2 solid 1px; padding: 2% 4%; border-radius: 15px;">
                    <h3>%s</h3>
                    <small>%s</small>        
                    <p>%s...
                    </p>
                    <a style="background-color: #660616; color: white; text-decoration: none; border: #660616 solid 1px; padding: 1% 2%; border-radius: 15px;" role="button" href='https://bartolo.org/noticia/%s/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                        Continua Leyendo ...
                    </a>
                </div>
                <br>
                <div style="text-align: center;"><small>Síguenos en Nuestras Redes Sociales</small></div>
                <div class="grid-container">
                    <div style="text-align: center;"><a href="https://bit.ly/3dD0mGy">Facebook</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3fAINsK">Twitter</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3ewUEXl">YouTube</a></div>
                </div>       

                <p style="color:#555555; text-align: center;">Centro Fray Bartolomé de las Casas &copy; 1998-2020</p>
            </body>
        </html>
    """ % (title, date, resumen, pk)
    email = EmailMessage(
                "Nueva Noticia · Centro Fray Bartolomé de las Casas", 
                cuerpo,
                to=correos,
    )
    email.content_subtype = "html" 
    email.send(fail_silently=True)

@background(schedule=5)
def twittertweet(pk, title, resumen, seccion="noticia"):
    consumer_key = "NY7kBN9ptV6IUn49lSlkerN0"
    consumer_secret = "Gd1SqdmY0tZzD1Rttxusrhm8w5OI2N5pMKHujYCC2dBAT3aRKH"
    access_token = "1254462238460710915-c5JweuGrookBEQfTFjkuXWLXyI9OoV"
    access_token_secret = "0YLI7ULFMEJg1DBFc0B9qj0AfYNe81qfz6I4qq86bIoVz"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status("%s\n%s...\n%s\n#cfbc" % (title, resumen, "https://bartolo.org/%s/%s/?utm_source=twitter-tweet&utm_medium=twitter&utm_campaign=crecimiento" % (seccion, pk)))

@background(schedule=5)
def facebookposts(pk, title, resumen, seccion="noticia"):
    token = "EAAUmfSh3VGABAFbD30GbVHxQfppNkGbstVZCseaKE0cHhHWmKSkR94VPVjMDZC6wx0i7b33sWu272ACUreJLDNj10li90pTv8OZA06EJDRvvnVkDsObS8226GKv3zdiv2QQe3ZCHihvNA9p0ajaXqa974ouhKZBbpyWGZCCrXtKFTu6H6OcNW1G2T4hmYau7TTW9yn31ZB92wZDZD"
    graph = facebook.GraphAPI(access_token=token, version="2.12")
    graph.put_object(
        parent_object='108435717211122', 
        connection_name='feed',
        message="%s\n%s...\Leer más" % (title, resumen),
        link="https://bartolo.org/%s/%s/?utm_source=facebook-posts&utm_medium=facebook&utm_campaign=crecimiento" % (seccion, pk)
    )

@background(schedule=5)
def enviar_evento_suscriptores(pk, title, resumen):
    correos = []
    for suscriptor in Suscriptor.objects.all().only('email'):
        correos.append(suscriptor.email)
    cuerpo = """
        <html>
            <head>
                <style>
                    body {
                        width: 75%;
                        margin: auto;
                        padding: 5%;
                    }
                    h1 {
                        text-align: center;
                        color: #660616;
                    }
                    .grid-container {
                        display: grid;
                        grid-template-columns: auto auto auto;
                        grid-gap: 10px;
                        padding: 5%;
                    }
                </style>
            </head>
            <body>        
                <div class="grid-container"> 
                    <div><h1>¡Nuevo Evento!</h1></div>           
                    <div style="text-align: right;">
                        <a href='https://bartolo.org/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                            <img src="https://bartolo.org/static/img/cfbc.png" alt="Centro Fray Bartolomé de las Casas" height="50vh" />
                        </a>
                    </div>
                </div>
                <div style="border: #e6e2e2 solid 1px; padding: 2% 4%; border-radius: 15px;">
                    <h3>%s</h3>        
                    <p>%s...
                    </p>
                    <a style="background-color: #660616; color: white; text-decoration: none; border: #660616 solid 1px; padding: 1% 2%; border-radius: 15px;" role="button" href='https://bartolo.org/evento/%s/?utm_source=correos-suscripcion&utm_medium=correo&utm_campaign=crecimiento'>
                        Más detalles ...
                    </a>
                </div>
                <br>
                <div style="text-align: center;"><small>Síguenos en Nuestras Redes Sociales</small></div>
                <div class="grid-container">
                    <div style="text-align: center;"><a href="https://bit.ly/3dD0mGy">Facebook</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3fAINsK">Twitter</a></div>
                    <div style="text-align: center;"><a href="https://bit.ly/3ewUEXl">YouTube</a></div>
                </div>       

                <p style="color:#555555; text-align: center;">Centro Fray Bartolomé de las Casas &copy; 1998-2020</p>
            </body>
        </html>
    """ % (title, resumen, pk)
    email = EmailMessage(
                "Nuevo Evento · Centro Fray Bartolomé de las Casas", 
                cuerpo,
                to=correos,
    )
    email.content_subtype = "html" 
    email.send(fail_silently=True)

