# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20141210_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='name',
            field=models.CharField(blank=True, verbose_name='英文名', max_length=200),
            preserve_default=True,
        ),
    ]
