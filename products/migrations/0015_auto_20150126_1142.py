# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20150126_1122'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fobprice',
            unique_together=set([('user', 'money_type', 'price_range_min', 'price_range_max', 'price_unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='moq',
            unique_together=set([('user', 'min_order_quantity', 'min_order_unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='supplyability',
            unique_together=set([('user', 'supply_quantity', 'supply_unit', 'supply_period')]),
        ),
    ]
