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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('level', models.IntegerField(verbose_name='目录级别', default=0)),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('parent', models.ForeignKey(null=True, to='products.Category', verbose_name='上级目录', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
