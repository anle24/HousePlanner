# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseplanner', '0012_auto_20170330_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.FloatField(),
        ),
    ]
