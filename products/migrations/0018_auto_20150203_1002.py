# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_extend_upload_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attr',
            name='value',
            field=models.CharField(verbose_name='属性值', max_length=200),
            preserve_default=True,
        ),
    ]
