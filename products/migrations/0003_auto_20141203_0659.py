# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20141203_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='cost',
            field=models.FloatField(verbose_name='成本'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='gross_weight',
            field=models.FloatField(verbose_name='毛重'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='net_weight',
            field=models.FloatField(verbose_name='净重'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='volume_weight',
            field=models.FloatField(verbose_name='积重'),
            preserve_default=True,
        ),
    ]
