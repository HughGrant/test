# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': '客户信息', 'verbose_name_plural': '客户信息'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': '国家信息', 'verbose_name_plural': '国家信息'},
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(verbose_name='地址', blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='code',
            field=models.CharField(verbose_name='邮编', blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='company',
            field=models.CharField(verbose_name='公司', blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='contact',
            field=models.CharField(verbose_name='号码', blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='country',
            field=models.ForeignKey(verbose_name='国家', to='clients.Country'),
            preserve_default=True,
        ),
    ]
