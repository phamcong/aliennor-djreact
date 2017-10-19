# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecocases', '0009_auto_20171018_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='esm',
            name='votes',
        ),
        migrations.AlterField(
            model_name='ecocase',
            name='image_urls',
            field=models.CharField(blank=True, default='', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='ecocase',
            name='images',
            field=models.FileField(blank=True, null=True, upload_to='ecocases'),
        ),
        migrations.AlterField(
            model_name='ecocase',
            name='reference',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ecocase',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]