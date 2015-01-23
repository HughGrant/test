# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20150122_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extend',
            name='is_markdown',
        ),
        migrations.AlterField(
            model_name='extend',
            name='rich_text',
            field=models.TextField(max_length=50000, blank=True, verbose_name='产品正文'),
            preserve_default=True,
        ),
    ]
