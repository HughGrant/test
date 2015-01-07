# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='last',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
