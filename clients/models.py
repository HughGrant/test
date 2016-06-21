#-*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Country(models.Model):
    # public info to all users, only superuser can do CRUD
    ibt_id = models.IntegerField('IBT_ID')
    cn_name = models.CharField('中文名', max_length=50)
    en_name = models.CharField('英文名', max_length=50)
    code = models.CharField('代码', max_length=10)
    voltage = models.CharField('电压', max_length=50)
    socket = models.CharField('插头', max_length=50)

    def __str__(self):
        return self.cn_name

    class Meta:
        verbose_name = verbose_name_plural = '国家信息'


@python_2_unicode_compatible
class Client(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField('姓名', max_length=200)
    email = models.EmailField('邮箱', blank=True)
    company = models.CharField('公司', blank=True, max_length=200)
    country = models.ForeignKey(
        Country, verbose_name='国家', blank=True, null=True)

    def __str__(self):
        return '%s(%s)' % (self.name, self.country)

    class Meta:
        verbose_name = verbose_name_plural = '客户信息'


@python_2_unicode_compatible
class Address(models.Model):
    client = models.ForeignKey('Client', verbose_name='所属客户')
    name = models.CharField('姓名', max_length=200)
    address = models.TextField('地址', blank=True, max_length=500)
    code = models.CharField('邮编', blank=True, max_length=200)
    contact = models.CharField('联系号码', blank=True, max_length=200)
    country = models.ForeignKey(
        Country, verbose_name='国家', blank=True, null=True)

    def __str__(self):
        return '%s(%s)' % (self.name, self.country)

    class Meta:
        verbose_name = verbose_name_plural = '地址信息'


@python_2_unicode_compatible
class LoginEmail(models.Model):
    user = models.ForeignKey(User)
    login_id = models.CharField('LoginID', blank=True, max_length=100)
    email = models.CharField('邮箱', blank=True, max_length=100)

    def __str__(self):
        return '%s(%s)' % (self.login_id, self.email)

    class Meta:
        verbose_name = verbose_name_plural = '帐户设置'
