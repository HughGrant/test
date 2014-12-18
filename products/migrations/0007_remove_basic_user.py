# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20141208_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basic',
            name='user',
        ),
    ]
