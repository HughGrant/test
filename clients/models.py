from django.db import models
from preset import VOLTAGE_CHOICES, SOCKET_CHOICES


class Country(models.Model):
    ibt_id = models.IntegerField('IBT_ID')
    cn_name = models.CharField('中文名', max_length=20)
    en_name = models.CharField('英文名', max_length=20)
    code = models.CharField('代码', max_length=10)
    voltage = models.IntegerField('电压', choices=VOLTAGE_CHOICES)
    socket = models.IntegerField('插头', choices=SOCKET_CHOICES)

    def __str__(self):
        return self.cn_name

    class Meta:
        verbose_name = verbose_name_plural = '国家信息'


class Client(models.Model):
    name = models.CharField('姓名', max_length=200)
    email = models.EmailField('邮箱')
    address = models.CharField('地址', blank=True, max_length=200)
    code = models.CharField('邮编', blank=True, max_length=200)
    contact = models.CharField('号码', blank=True, max_length=200)
    company = models.CharField('公司', blank=True, max_length=200)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '客户信息'
