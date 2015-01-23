# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0011_auto_20150122_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='fobprice',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moq',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplyability',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=2),
            preserve_default=False,
        ),
    ]
