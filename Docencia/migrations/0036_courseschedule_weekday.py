# Generated by Django 3.0.4 on 2020-08-17 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Docencia', '0035_auto_20200817_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseschedule',
            name='weekday',
            field=models.CharField(choices=[('Lun.', 'Lunes'), ('Mar.', 'Martes'), ('Mié.', 'Miércoles'), ('Jue.', 'Jueves'), ('Vie.', 'Viernes'), ('Sáb.', 'Sábado')], default='Lun.', max_length=4),
        ),
    ]