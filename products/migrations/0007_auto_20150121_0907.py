# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20150121_0741'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fobprice',
            old_name='price_uint',
            new_name='price_unit',
        ),
    ]
