# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_category_ali_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='basic',
            name='keyword',
            field=models.CharField(verbose_name='默认主关键字', blank=True, max_length=200),
            preserve_default=True,
        ),
    ]
