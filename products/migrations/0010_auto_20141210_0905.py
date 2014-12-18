# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20141208_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='basic',
            name='cn_name',
            field=models.CharField(max_length=200, default='', verbose_name='中文名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='basic',
            name='name',
            field=models.CharField(max_length=200, verbose_name='英文名'),
            preserve_default=True,
        ),
    ]
