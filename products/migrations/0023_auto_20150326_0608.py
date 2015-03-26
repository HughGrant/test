# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_differentprice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='differentprice',
            options={'verbose_name_plural': '产品差异价', 'verbose_name': '产品差异价'},
        ),
        migrations.AlterField(
            model_name='differentprice',
            name='price',
            field=models.FloatField(verbose_name='价钱', default=0),
            preserve_default=True,
        ),
    ]
