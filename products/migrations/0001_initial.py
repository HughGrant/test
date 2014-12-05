# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='产品名', max_length=200)),
                ('model', models.CharField(verbose_name='型号', max_length=200)),
                ('video', models.CharField(verbose_name='视频', max_length=200)),
                ('size', models.CharField(verbose_name='尺寸', max_length=200)),
                ('net_weight', models.FloatField(verbose_name='净重', max_length=200)),
                ('gross_weight', models.FloatField(verbose_name='毛重', max_length=200)),
                ('volume_weight', models.FloatField(verbose_name='积重', max_length=200)),
                ('cost', models.CharField(verbose_name='成本', max_length=200)),
                ('voltage', models.CharField(verbose_name='电压', max_length=200)),
                ('bak', models.TextField(verbose_name='备注', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
