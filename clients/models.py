from django.db import models
from django.contrib.auth.models import User


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


class Client(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField('姓名', max_length=200)
    email = models.EmailField('邮箱', blank=True)
    address = models.CharField('地址', blank=True, max_length=200)
    code = models.CharField('邮编', blank=True, max_length=200)
    contact = models.CharField('号码', blank=True, max_length=200)
    company = models.CharField('公司', blank=True, max_length=200)
    country = models.ForeignKey(
        Country, verbose_name='国家', blank=True, null=True)

    def __str__(self):
        return '%s(%s)' % (self.name, self.country)

    class Meta:
        verbose_name = verbose_name_plural = '客户信息'
