# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20150331_0741'),
        ('products', '0026_auto_20150331_0828'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(default=0, verbose_name='总成本')),
                ('shipping_cost', models.FloatField(default=0, verbose_name='总运费')),
                ('total_price', models.FloatField(default=0, verbose_name='总报价')),
                ('bak', models.TextField(verbose_name='备注', max_length=500, blank=True)),
                ('date', models.DateField(verbose_name='日期', auto_now_add=True)),
                ('client', models.ForeignKey(verbose_name='客户', to='clients.Client', blank=True, null=True)),
            ],
            options={
                'verbose_name': '定单',
                'verbose_name_plural': '定单',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender_info', models.CharField(verbose_name='付款人信息', max_length=100, blank=True)),
                ('collected_money', models.FloatField(default=0, verbose_name='收款金额')),
                ('currency_type', models.IntegerField(default=1, verbose_name='货币类型', choices=[(1, 'USD'), (2, 'RMB'), (3, 'EUR'), (5, 'GBP'), (6, 'JPY'), (7, 'AUD'), (8, 'CAD'), (9, 'CHF'), (11, 'NTD'), (12, 'HKD'), (13, 'NZD'), (4, 'Other')])),
                ('exchange_rate', models.FloatField(default=6.2, verbose_name='对人民币汇率')),
                ('payment_method', models.IntegerField(default=1, verbose_name='付款方式', choices=[(0, '未付款'), (1, 'PAYPAL'), (2, '西联'), (3, 'T/T'), (4, '国内银行转账'), (5, 'L/C'), (6, 'D/A'), (7, 'D/P'), (8, 'MoneyGram')])),
                ('verified', models.BooleanField(default=False, verbose_name='是否已核实付款')),
                ('date', models.DateField(verbose_name='日期', auto_now_add=True)),
                ('bak', models.CharField(verbose_name='备注', max_length=200, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '付款信息',
                'verbose_name_plural': '付款信息',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0, verbose_name='数量')),
                ('cost', models.FloatField(default=0, verbose_name='成本')),
                ('price', models.FloatField(default=0, verbose_name='单价')),
                ('bak', models.CharField(verbose_name='备注', max_length=200, blank=True)),
                ('order', models.ForeignKey(to='buss.Order')),
                ('product', models.ForeignKey(to='products.Basic')),
            ],
            options={
                'verbose_name': '定单内容',
                'verbose_name_plural': '定单内容',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(verbose_name='付款信息', to='buss.Payment', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
