# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20141203_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='类目', max_length=200)),
                ('word', models.CharField(verbose_name='类目', max_length=200)),
                ('count', models.IntegerField(verbose_name='计数', default=0)),
            ],
            options={
                'verbose_name': '产品关键字',
                'verbose_name_plural': '产品关键字',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='basic',
            options={'verbose_name': '产品基本信息', 'verbose_name_plural': '产品基本信息'},
        ),
        migrations.AlterField(
            model_name='basic',
            name='bak',
            field=models.TextField(verbose_name='备注', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='cost',
            field=models.FloatField(verbose_name='成本(RMB)', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='gross_weight',
            field=models.FloatField(verbose_name='毛重', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='model',
            field=models.CharField(verbose_name='型号', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='net_weight',
            field=models.FloatField(verbose_name='净重', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='size',
            field=models.CharField(verbose_name='尺寸', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='video',
            field=models.CharField(verbose_name='视频', max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basic',
            name='volume_weight',
            field=models.FloatField(verbose_name='积重', default=0),
            preserve_default=True,
        ),
    ]
