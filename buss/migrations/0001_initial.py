# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('total_cost', models.FloatField(verbose_name='总成本', default=0)),
                ('shipping_cost', models.FloatField(verbose_name='总运费', default=0)),
                ('total_price', models.FloatField(verbose_name='总报价', default=0)),
                ('bak', models.TextField(verbose_name='备注', blank=True, max_length=500)),
                ('date', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('client', models.ForeignKey(null=True, blank=True, verbose_name='客户', to='clients.Client')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('collected_money', models.FloatField(verbose_name='收款金额', default=0)),
                ('currency_type', models.CharField(verbose_name='货币类型', choices=[('US', 'USD'), ('CH', 'RMB'), ('EU', 'EUR'), ('GB', 'GBP'), ('JP', 'JPY'), ('AU', 'AUD'), ('CA', 'CAD'), ('CF', 'CHF'), ('NT', 'NTD'), ('HK', 'HKD'), ('NZ', 'NZD'), ('OT', 'Other')], max_length=8, default='US')),
                ('exchange_rate', models.FloatField(verbose_name='对人民币汇率', default=6.0)),
                ('payment_method', models.IntegerField(verbose_name='付款方式', choices=[(0, '未付款'), (1, 'PAYPAL'), (2, '西联'), (3, 'T/T'), (4, '国内银行转账')], default=0)),
                ('verified', models.BooleanField(verbose_name='是否已核实', default=False)),
                ('date', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('bak', models.CharField(verbose_name='备注', blank=True, max_length=200)),
                ('creator', models.ForeignKey(related_name='+', verbose_name='创建者', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(null=True, blank=True, to='buss.Order')),
            ],
            options={
                'verbose_name': '付款信息',
                'verbose_name_plural': '付款信息',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentIssue',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('issue', models.TextField(verbose_name='纠纷内容', max_length=1000)),
                ('date', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('handled', models.BooleanField(verbose_name='是还已处理', default=False)),
                ('handle_date', models.DateField(null=True, verbose_name='处理日期')),
                ('creator', models.ForeignKey(related_name='+', verbose_name='创建者', to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(to='buss.Payment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='所属人')),
            ],
            options={
                'verbose_name': '纠纷',
                'verbose_name_plural': '纠纷',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('quantity', models.IntegerField(verbose_name='数量', default=0)),
                ('cost', models.FloatField(verbose_name='成本', default=0)),
                ('price', models.FloatField(verbose_name='单价', default=0)),
                ('bak', models.CharField(verbose_name='备注', blank=True, max_length=200)),
                ('order', models.ForeignKey(to='buss.Order')),
                ('product', models.ForeignKey(to='products.Basic')),
            ],
            options={
                'verbose_name': '定单内容',
                'verbose_name_plural': '定单内容',
            },
            bases=(models.Model,),
        ),
    ]
