# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20150121_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extend',
            name='packaging_desc',
            field=models.CharField(max_length=600, verbose_name='包装描述'),
            preserve_default=True,
        ),
    ]
