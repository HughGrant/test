# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buss', '0003_auto_20150121_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.IntegerField(default=0, verbose_name='付款方式', choices=[(0, '未付款'), (1, 'PAYPAL'), (2, '西联'), (3, 'T/T'), (4, '国内银行转账'), (5, 'L/C'), (6, 'D/A'), (7, 'D/P'), (8, 'MoneyGram')]),
            preserve_default=True,
        ),
    ]
