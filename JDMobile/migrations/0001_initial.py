# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('PID', models.AutoField(default='', primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
