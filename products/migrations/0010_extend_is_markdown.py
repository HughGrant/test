# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20150121_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='extend',
            name='is_markdown',
            field=models.BooleanField(default=False, verbose_name='是否为Markdown'),
            preserve_default=True,
        ),
    ]
