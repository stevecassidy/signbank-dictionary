# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-09 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20170601_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialect',
            name='index',
            field=models.IntegerField(default=1),
        ),
    ]