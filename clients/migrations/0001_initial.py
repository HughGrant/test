# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=200)),
                ('email', models.EmailField(verbose_name='邮箱', max_length=75)),
                ('address', models.CharField(verbose_name='地址', blank=True, max_length=200)),
                ('code', models.CharField(verbose_name='邮编', blank=True, max_length=200)),
                ('contact', models.CharField(verbose_name='号码', blank=True, max_length=200)),
                ('company', models.CharField(verbose_name='公司', blank=True, max_length=200)),
            ],
            options={
                'verbose_name': '客户信息',
                'verbose_name_plural': '客户信息',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('ibt_id', models.IntegerField(verbose_name='IBT_ID')),
                ('cn_name', models.CharField(verbose_name='中文名', max_length=20)),
                ('en_name', models.CharField(verbose_name='英文名', max_length=20)),
                ('code', models.CharField(verbose_name='代码', max_length=10)),
                ('voltage', models.IntegerField(verbose_name='电压', choices=[(0, '无电压'), (220, '220V'), (110, '110V')])),
                ('socket', models.IntegerField(verbose_name='插头', choices=[(0, '国标'), (1, '英标'), (2, '美标'), (3, '意标'), (4, '南非标'), (5, '瑞士标'), (6, '欧标(德标)')])),
            ],
            options={
                'verbose_name': '国家信息',
                'verbose_name_plural': '国家信息',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='client',
            name='country',
            field=models.ForeignKey(to='clients.Country', verbose_name='国家'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
