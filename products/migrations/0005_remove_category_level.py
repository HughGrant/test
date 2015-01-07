# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20150106_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='level',
        ),
    ]
