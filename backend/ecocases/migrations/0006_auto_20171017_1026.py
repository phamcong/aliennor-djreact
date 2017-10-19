# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 10:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecocases', '0005_auto_20171016_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('vote_point', models.IntegerField(default=0)),
                ('esm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecocases.ESM')),
            ],
        ),
        migrations.AlterField(
            model_name='ecocase',
            name='proven_cas_or_project',
            field=models.CharField(choices=[('Project', 'Project'), ('Proven cas', 'Proven cas')], default='project', max_length=20),
        ),
    ]
