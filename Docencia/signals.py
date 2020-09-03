from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# import locale
# locale.setlocale(locale.LC_TIME, "es_CU")

from Docencia.tasks import enviar_suscriptores, twittertweet, facebookposts
from Docencia.Index.models import News, Events

@receiver(post_save, sender=News)
def signal_enviar_email(sender, instance, **kwargs):
    if (kwargs.get('created', False)):
        delta = instance.date - timezone.now()
        enviar_suscriptores(
            instance.pk, 
            instance.title, 
            instance.body[:100], 
            instance.date.strftime("%a %d %b %Y %H:%M").title(), 
            schedule=delta
        )

        twittertweet(
            instance.pk,
            instance.title,
            instance.body[:100],
            schedule=delta
        )

        facebookposts(
            instance.pk,
            instance.title,
            instance.body[:100],
            schedule=delta
        )

@receiver(post_save, sender=Events)
def signal_enviar_evento(sender, instance, **kwargs):
    if (kwargs.get("created", False)):
        enviar_evento_suscriptores(
            instance.pk,
            instance.name,
            instance.body,
            schedule=timezone.now()
        )
        twittertweet(
            instance.pk,
            instance.name,
            instance.body,
            'evento',
            schedule=timezone.now()
        )

        facebookposts(
            instance.pk,
            instance.name,
            instance.body,
            'evento',
            schedule=timezone.now()
        )

