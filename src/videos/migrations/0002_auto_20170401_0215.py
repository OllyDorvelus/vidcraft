# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='video',
            field=models.FileField(upload_to='video'),
        ),
    ]
