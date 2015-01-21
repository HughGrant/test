# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_extend_richtext'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attr',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='属性名')),
                ('value', models.CharField(max_length=100, verbose_name='属性值')),
                ('extend', models.ForeignKey(to='products.Extend', verbose_name='产品详细信息')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='extend',
            name='category',
            field=models.ForeignKey(to='products.Category', verbose_name='产品分类'),
            preserve_default=True,
        ),
    ]
