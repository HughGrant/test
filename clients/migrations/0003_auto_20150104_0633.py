# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_auto_20141231_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='en_name',
            field=models.CharField(verbose_name='英文名', max_length=30),
            preserve_default=True,
        ),
    ]
