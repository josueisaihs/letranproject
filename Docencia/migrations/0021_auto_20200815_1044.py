# Generated by Django 3.0.4 on 2020-08-15 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Docencia', '0020_auto_20200815_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headerindex',
            name='btn1',
            field=models.CharField(blank=True, max_length=10, verbose_name='Botón 1 Texto'),
        ),
        migrations.AlterField(
            model_name='headerindex',
            name='btn2',
            field=models.CharField(blank=True, max_length=10, verbose_name='Botón 2 Texto'),
        ),
    ]
