# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170301_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custompermission',
            options={'permissions': (('blog_admin', 'Blog administration'), ('portfolio_admin', 'Portfolio administration'), ('testimonials_admin', 'Testimonials administration'), ('projects_admin', 'Projects administration'), ('contact_us', 'Permission to see customer messages'), ('admin_users', 'Admin users administration'), ('general_users', 'General users administration'))},
        ),
    ]
