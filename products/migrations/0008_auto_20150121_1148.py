# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20150121_0907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='richtext',
            name='extend',
        ),
        migrations.DeleteModel(
            name='RichText',
        ),
        migrations.AddField(
            model_name='extend',
            name='rich_text',
            field=models.TextField(default='', verbose_name='产品正文', max_length=50000),
            preserve_default=False,
        ),
    ]
