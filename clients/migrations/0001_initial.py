# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=200)),
                ('email', models.EmailField(verbose_name='邮箱', max_length=75)),
                ('address', models.CharField(verbose_name='地址', max_length=200)),
                ('code', models.CharField(verbose_name='邮编', max_length=200)),
                ('contact', models.CharField(verbose_name='号码', max_length=200)),
                ('company', models.CharField(verbose_name='公司', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('ibt_id', models.IntegerField(verbose_name='IBT_ID')),
                ('cn_name', models.CharField(verbose_name='中文名', max_length=20)),
                ('en_name', models.CharField(verbose_name='英文名', max_length=20)),
                ('code', models.CharField(verbose_name='代码', max_length=10)),
                ('voltage', models.IntegerField(choices=[(0, '无电压'), (220, '220V'), (110, '110V')], verbose_name='电压')),
                ('socket', models.IntegerField(choices=[(0, '国标'), (1, '英标'), (2, '美标'), (3, '意标'), (4, '南非标'), (5, '瑞士标'), (6, '欧标(德标)')], verbose_name='插头')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='client',
            name='country',
            field=models.ForeignKey(to='clients.Country'),
            preserve_default=True,
        ),
    ]
