from background_task import background

from django.core.mail import EmailMessage, BadHeaderError, send_mass_mail
from smtplib import SMTPException
from django.contrib.auth.models import User

from Docencia.Index.models import Suscriptor

from validate_email import validate_email

import logging
logger = logging.getLogger(__name__)

@background(schedule=10)
def notify_user(user_id):
    # lookup user by id and send them a message
    print("Enviando")
    user = User.objects.get(pk=user_id)
    user.email_user('Here is a notification', 'You have been notified')

@background(schedule=5)
def verificar_email(_email_):
    print("Verificando: %s" % _email_)
    try:
        email = EmailMessage(
                "Centro Fray Bartolomé de las Casas", 
                "Se ha suscrito en el Centro Fray Bartolomé de las Casas.",
                to=[_email_],
        )
        if validate_email(_email_, verify=True):
            logger.info("Suscrito: <%s>" % _email_)
            email.send(fail_silently=False)
            print("validado: %s" % _email_)
        else:
            suscriptor = Suscriptor.objects.get(email=_email_)
            suscriptor.delete()
            logger.warning("El email <%s>" % _email_)
            print("No existe emial: %s" % _email_)
    except TimeoutError as e:
        logger.exception("Error: TimeoutError %s" % _email_)
        print("Error timeout")

@background(schedule=5)
def enviar_suscriptores(pk:int, title:str, resumen:str, date:str):
    print(pk, title, resumen, date)
    correos = []
    for suscriptor in Suscriptor.objects.all().only('email'):
        correos.append(suscriptor.email)
    print(correos)
    cuerpo = ""
    email = EmailMessage(
                "Nueva Noticia · Centro Fray Bartolomé de las Casas", 
                "<html><head></head><body><strong>¡Nueva Noticia!</strong><br><hr><h1>%s</h1><br><small>%s</small>" % (title, date) +
                "<p>%s...</p>" % resumen +
                "<a href='https://bartolo.org/noticia/%s/'>Leer Más ...</a><br><br>" % pk +
                "<a href='https://bartolo.org'><small>Centro Fray Bartolomé de las Casas</small></a></body></html>",
                to=correos,
    )
    email.content_subtype = "html" 
    email.send(fail_silently=True)
