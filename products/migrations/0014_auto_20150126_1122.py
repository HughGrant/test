# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20150122_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='voltage',
            field=models.IntegerField(choices=[(0, '无电压'), (1, '气动'), (220, '220V'), (110, '110V')], default=0, verbose_name='电压'),
            preserve_default=True,
        ),
    ]
