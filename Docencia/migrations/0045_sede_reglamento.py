# Generated by Django 3.1 on 2020-08-24 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Docencia', '0044_auto_20200824_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='sede',
            name='reglamento',
            field=models.FileField(blank=True, null=True, upload_to='static/sedes/reglamentos', verbose_name='Reglamento'),
        ),
    ]
