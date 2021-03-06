# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-01 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='role',
            field=models.CharField(choices=[('auslan', 'Definition in Auslan'), ('general', 'General Definition'), ('noun', 'As a Noun'), ('verb', 'As a Verb or Adjective'), ('deictic', 'As a Pointing Sign'), ('interact', 'Interactive'), ('modifier', 'As Modifier'), ('question', 'As Question'), ('popexplain', 'Popular Explanation'), ('augment', 'Augmented Meaning'), ('note', 'Note'), ('privatenote', 'Private Note'), ('B92 sn', 'Sign Number in Brien 92')], max_length=20),
        ),
        migrations.AlterField(
            model_name='definition',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
