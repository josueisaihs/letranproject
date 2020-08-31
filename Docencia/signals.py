from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# import locale
# locale.setlocale(locale.LC_TIME, "es_CU")

from Docencia.tasks import enviar_suscriptores
from Docencia.Index.models import News

@receiver(post_save, sender=News)
def signal_enviar_email(sender, instance, **kwargs):
    if (kwargs.get('created', False)):
        delta = instance.date - timezone.now()
        enviar_suscriptores(instance.pk, instance.title, instance.body[:30], instance.date.strftime("%a %d %b %Y %H:%M").title(), schedule=delta)