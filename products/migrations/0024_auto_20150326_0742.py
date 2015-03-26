# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20150326_0608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('difference', models.CharField(max_length=100, verbose_name='描述')),
                ('price', models.FloatField(default=0, verbose_name='价钱(RMB)')),
                ('basic', models.ForeignKey(to='products.Basic', verbose_name='产品基本信息')),
            ],
            options={
                'verbose_name_plural': '产品配件',
                'verbose_name': '产品配件',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='differentprice',
            name='price',
            field=models.FloatField(default=0, verbose_name='价钱(RMB)'),
            preserve_default=True,
        ),
    ]
