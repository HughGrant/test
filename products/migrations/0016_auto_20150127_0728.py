# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20150126_1142'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fobprice',
            unique_together=set([('money_type', 'price_range_min', 'price_range_max', 'price_unit')]),
        ),
        migrations.RemoveField(
            model_name='fobprice',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='moq',
            unique_together=set([('min_order_quantity', 'min_order_unit')]),
        ),
        migrations.RemoveField(
            model_name='moq',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='supplyability',
            unique_together=set([('supply_quantity', 'supply_unit', 'supply_period')]),
        ),
        migrations.RemoveField(
            model_name='supplyability',
            name='user',
        ),
    ]
