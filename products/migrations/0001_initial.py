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
            name='Basic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('cn_name', models.CharField(verbose_name='中文名', max_length=200)),
                ('name', models.CharField(verbose_name='英文名', blank=True, max_length=200)),
                ('model', models.CharField(verbose_name='型号', blank=True, max_length=200)),
                ('video', models.CharField(verbose_name='视频', blank=True, max_length=200)),
                ('size', models.CharField(verbose_name='尺寸', blank=True, max_length=200)),
                ('net_weight', models.FloatField(verbose_name='净重(KG)', default=0)),
                ('gross_weight', models.FloatField(verbose_name='毛重(KG)', default=0)),
                ('volume_weight', models.FloatField(verbose_name='积重(KG)', default=0)),
                ('cost', models.FloatField(verbose_name='成本(RMB)', default=0)),
                ('voltage', models.IntegerField(verbose_name='电压', choices=[(0, '无电压'), (220, '220V'), (110, '110V')])),
                ('bak', models.TextField(verbose_name='备注', blank=True, max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '产品基本信息',
                'verbose_name_plural': '产品基本信息',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='类目', max_length=200)),
                ('word', models.CharField(verbose_name='关键字', max_length=200)),
                ('count', models.IntegerField(verbose_name='使用计数', default=0)),
            ],
            options={
                'verbose_name': '产品关键字',
                'verbose_name_plural': '产品关键字',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together=set([('name', 'word')]),
        ),
    ]
