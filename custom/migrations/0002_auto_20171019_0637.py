# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 06:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='group',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='roles',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='UserGroup',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
