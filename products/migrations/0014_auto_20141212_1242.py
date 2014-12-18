# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20141210_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='gross_weight',
            field=models.FloatField(default=0, verbose_name='毛重(KG)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='net_weight',
            field=models.FloatField(default=0, verbose_name='净重(KG)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='volume_weight',
            field=models.FloatField(default=0, verbose_name='积重(KG)'),
            preserve_default=True,
        ),
    ]
