# Generated by Django 3.0.4 on 2020-08-16 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Docencia', '0026_auto_20200816_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='section',
            field=models.CharField(choices=[('enl', 'Enlaces Útiles'), ('opr', 'Orden Predicadores')], default='enl', max_length=3, verbose_name='Sección'),
        ),
    ]
