# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-03-21 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
            ],
        ),
    ]