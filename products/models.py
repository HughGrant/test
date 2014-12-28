from django.db import models
from django.contrib.auth.models import User
from preset import VOLTAGE_CHOICES


class Basic(models.Model):
    user = models.ForeignKey(User)
    cn_name = models.CharField('中文名', max_length=200)
    name = models.CharField('英文名', blank=True, max_length=200)
    model = models.CharField('型号', blank=True, max_length=200)
    video = models.CharField('视频', blank=True, max_length=200)
    size = models.CharField('尺寸', blank=True, max_length=200)
    net_weight = models.FloatField('净重(KG)', default=0)
    gross_weight = models.FloatField('毛重(KG)', default=0)
    volume_weight = models.FloatField('积重(KG)', default=0)
    cost = models.FloatField('成本(RMB)', default=0)
    voltage = models.IntegerField('电压', choices=VOLTAGE_CHOICES)
    bak = models.TextField('备注', blank=True, max_length=200)

    def __str__(self):
        return "%s(%s)" % (self.cn_name, self.model)

    def weight(self):
        return max([self.net_weight, self.gross_weight, self.volume_weight])
    weight.short_description = '重量(KG)'

    class Meta:
        verbose_name = verbose_name_plural = '产品基本信息'


class Keyword(models.Model):
    name = models.CharField('类目', max_length=200)
    word = models.CharField('关键字', max_length=200)
    count = models.IntegerField('使用计数', default=0)

    def __str__(self):
        return "%s-%s" % (self.name, self.word)

    class Meta:
        unique_together = ('name', 'word')
        verbose_name = verbose_name_plural = '产品关键字'


# class Attr(models.Model):
#     basic = models.ForeignKey(Basic)
#     name = models.CharField('属性名', max_length=50)
#     value = models.CharField('属性值', max_length=50)


# class Extend(models.Model):
#     category = models.CharField('类目', max_length=100)
#     summary = models.CharField('概览', max_length=200)
#     # photos = models.CharField('产品图片', max_length=100)
#     # attrs = models.CharField('产品属性', max_length=100)
#     min_order_quantity = models.IntegerField('起订量', default=1)
#     # min_order_unit = models.CharField('起订单位', max_length=100)
#     money_type = models.CharField('货币类型', max_length=10, choices=CURRENCY_TYPE)
#     price_range_min = models.FloatField('最低报价', default=0)
#     price_range_max = models.FloatField('最高报价', default=0)
#     # price_uint = models.CharField('报价单位', max_length=10)
#     port = models.CharField('港口', max_length=100)
#     # payment_method = models.IntegerField('付款方式', default=0)
#     supply_quantity = models.IntegerField('产量', max_length=100)
#     # supply_unit = models.CharField('产量单位', max_length=100)
#     # supply_period = models.CharField('产量周期', max_length=100)
#     consignment_term = models.CharField('运输时长', max_length=100)
#     packaging_desc = models.CharField('包装描述', max_length=200)
#     rich_text = models.TextField('产品正文', max_length=200)
