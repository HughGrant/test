# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_basic_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='DifferentPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('difference', models.CharField(max_length=100, verbose_name='描述')),
                ('price', models.FloatField(verbose_name='价钱')),
                ('basic', models.ForeignKey(to='products.Basic', verbose_name='产品基本信息')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
