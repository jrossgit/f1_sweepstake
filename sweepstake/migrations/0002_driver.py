# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-01 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sweepstake', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drivers', to='sweepstake.Team')),
            ],
        ),
    ]
