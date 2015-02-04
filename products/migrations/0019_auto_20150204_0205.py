# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0018_auto_20150203_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basic',
            name='user',
        ),
        migrations.AddField(
            model_name='extend',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=2),
            preserve_default=False,
        ),
    ]
