# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-24 22:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sweepstake', '0003_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(blank=True, null=True)),
                ('classified', models.NullBooleanField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='sweepstake.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateField(unique=True)),
            ],
        ),
        migrations.AlterOrderWithRespectTo(
            name='race',
            order_with_respect_to='date',
        ),
        migrations.AddField(
            model_name='driverresult',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='sweepstake.Race'),
        ),
        migrations.AlterUniqueTogether(
            name='driverresult',
            unique_together=set([('race', 'position')]),
        ),
    ]
