# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20141210_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='cn_name',
            field=models.CharField(verbose_name='中文名', max_length=200),
            preserve_default=True,
        ),
    ]
