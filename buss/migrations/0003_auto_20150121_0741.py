# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buss', '0002_auto_20150114_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.IntegerField(default=0, verbose_name='付款方式', choices=[('PayPal', 'PayPal'), ('Western Union', 'Western Union'), ('T/T', 'T/T'), ('L/C', 'L/C'), ('D/A', 'D/A'), ('D/P', 'D/P'), ('MoneyGram', 'MoneyGram')]),
            preserve_default=True,
        ),
    ]
