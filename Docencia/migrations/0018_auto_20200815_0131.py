# Generated by Django 3.0.4 on 2020-08-15 01:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Docencia', '0017_auto_20200814_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='user',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='dateend',
            field=models.DateField(default=datetime.date(2021, 2, 11), verbose_name='Fecha de Fin'),
        ),
    ]