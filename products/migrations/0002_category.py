# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, verbose_name='类目名称')),
                ('parent', models.ForeignKey(null=True, to='products.Category', blank=True, verbose_name='上级类目')),
            ],
            options={
                'verbose_name': '产品分类',
                'verbose_name_plural': '产品分类',
            },
            bases=(models.Model,),
        ),
    ]
