# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='cn_name',
            field=models.CharField(max_length=30, verbose_name='中文名'),
            preserve_default=True,
        ),
    ]
