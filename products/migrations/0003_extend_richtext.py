# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extend',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('min_order_quantity', models.IntegerField(default=1, verbose_name='起订量')),
                ('money_type', models.CharField(max_length=10, verbose_name='货币类型', choices=[('US', 'USD'), ('CH', 'RMB'), ('EU', 'EUR'), ('GB', 'GBP'), ('JP', 'JPY'), ('AU', 'AUD'), ('CA', 'CAD'), ('CF', 'CHF'), ('NT', 'NTD'), ('HK', 'HKD'), ('NZ', 'NZD'), ('OT', 'Other')])),
                ('price_range_min', models.FloatField(default=0, verbose_name='最低报价')),
                ('price_range_max', models.FloatField(default=0, verbose_name='最高报价')),
                ('port', models.CharField(max_length=100, verbose_name='港口')),
                ('supply_quantity', models.IntegerField(max_length=100, verbose_name='产量')),
                ('consignment_term', models.CharField(max_length=100, verbose_name='运输时长')),
                ('packaging_desc', models.CharField(max_length=200, verbose_name='包装描述')),
                ('basic', models.ForeignKey(verbose_name='基本信息', to='products.Basic')),
                ('category', models.ForeignKey(to='products.Category')),
            ],
            options={
                'verbose_name_plural': '产品详细信息',
                'verbose_name': '产品详细信息',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RichText',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('introduction', models.TextField(blank=True, verbose_name='产品简介')),
                ('specification', models.TextField(blank=True, verbose_name='参数信息')),
                ('application', models.TextField(blank=True, verbose_name='适用范围')),
                ('package', models.TextField(blank=True, verbose_name='产品包装')),
                ('extend', models.ForeignKey(verbose_name='产品详细信息', to='products.Extend')),
            ],
            options={
                'verbose_name_plural': '产品正文信息',
                'verbose_name': '产品正文信息',
            },
            bases=(models.Model,),
        ),
    ]
