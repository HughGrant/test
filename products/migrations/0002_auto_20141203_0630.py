# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='voltage',
            field=models.IntegerField(verbose_name='电压', choices=[(0, '无电压'), (220, '220V'), (110, '110V')]),
            preserve_default=True,
        ),
    ]
