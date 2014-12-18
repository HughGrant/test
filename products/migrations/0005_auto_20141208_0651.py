# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20141204_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='basic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='keyword',
            name='count',
            field=models.IntegerField(verbose_name='使用计数', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keyword',
            name='word',
            field=models.CharField(verbose_name='关键字', max_length=200),
            preserve_default=True,
        ),
    ]
