# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20141208_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='user',
            field=models.ForeignKey(default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
