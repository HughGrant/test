# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_last'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '产品分类', 'verbose_name': '产品分类'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='last',
        ),
        migrations.AlterField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=0, verbose_name='类目级别'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(verbose_name='类目名称', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(to='products.Category', verbose_name='上级类目', null=True, blank=True),
            preserve_default=True,
        ),
    ]
