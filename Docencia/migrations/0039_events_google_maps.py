# Generated by Django 3.0.4 on 2020-08-17 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Docencia', '0038_auto_20200817_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='google_maps',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Embeber Google Maps'),
        ),
    ]