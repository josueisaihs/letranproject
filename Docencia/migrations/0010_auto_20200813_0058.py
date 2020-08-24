# Generated by Django 3.0.4 on 2020-08-13 00:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Docencia', '0009_courseinformation_programa'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='courseinformation',
            name='reglamento',
            field=models.FileField(blank=True, null=True, upload_to='static/cursos/programas', verbose_name='Reglamento'),
        ),
        migrations.AlterField(
            model_name='colaboradores',
            name='labor',
            field=models.TextField(max_length=1000, verbose_name='Labor'),
        ),
        migrations.AlterField(
            model_name='courseinformation',
            name='programa',
            field=models.FileField(blank=True, null=True, upload_to='static/cursos/programas', verbose_name='Programa'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='dateend',
            field=models.DateField(default=datetime.date(2021, 2, 9), verbose_name='Fecha de Fin'),
        ),
    ]