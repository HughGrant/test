# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20150104_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='cn_name',
            field=models.CharField(max_length=50, verbose_name='中文名'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='country',
            name='en_name',
            field=models.CharField(max_length=50, verbose_name='英文名'),
            preserve_default=True,
        ),
    ]
