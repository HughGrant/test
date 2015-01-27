# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20150104_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='voltage',
            field=models.IntegerField(choices=[(0, '无电压'), (1, '气动'), (220, '220V'), (110, '110V')], verbose_name='电压'),
            preserve_default=True,
        ),
    ]
