# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buss', '0002_remove_payment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='bak',
            field=models.CharField(max_length=200, verbose_name='备注', blank=True),
            preserve_default=True,
        ),
    ]
