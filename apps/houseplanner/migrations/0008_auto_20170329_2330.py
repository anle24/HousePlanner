# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 23:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseplanner', '0007_auto_20170329_2229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='date',
            new_name='startDate',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
        migrations.AddField(
            model_name='event',
            name='endDate',
            field=models.DateField(default=datetime.date(2017, 3, 29)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='endTime',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='startTime',
            field=models.TimeField(null=True),
        ),
    ]
