# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_basic_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together=set([('name', 'word')]),
        ),
    ]
