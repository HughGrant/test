# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency_type',
            field=models.CharField(choices=[(1, 'USD'), (2, 'RMB'), (3, 'EUR'), (5, 'GBP'), (6, 'JPY'), (7, 'AUD'), (8, 'CAD'), (9, 'CHF'), (11, 'NTD'), (12, 'HKD'), (13, 'NZD'), (4, 'Other')], max_length=8, verbose_name='货币类型', default='US'),
            preserve_default=True,
        ),
    ]
