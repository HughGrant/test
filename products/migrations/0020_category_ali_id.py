# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20150204_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='ali_id',
            field=models.IntegerField(verbose_name='阿里ID', default=0),
            preserve_default=True,
        ),
    ]
