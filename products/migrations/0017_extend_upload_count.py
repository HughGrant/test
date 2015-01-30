# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20150127_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='extend',
            name='upload_count',
            field=models.IntegerField(default=0, verbose_name='已上传次数'),
            preserve_default=True,
        ),
    ]
