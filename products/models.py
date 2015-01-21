from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.filelds import ArrayField
from preset import *


class Basic(models.Model):
    user = models.ForeignKey(User)
    cn_name = models.CharField('中文名', blank=True, max_length=200)
    name = models.CharField('英文名', blank=True, max_length=200)
    model = models.CharField('型号', blank=True, max_length=200)
    video = models.CharField('视频', blank=True, max_length=200)
    size = models.CharField('尺寸(CM)', blank=True, max_length=200)
    net_weight = models.FloatField('净重(KG)', default=0)
    gross_weight = models.FloatField('毛重(KG)', default=0)
    volume_weight = models.FloatField('积重(KG)', default=0)
    cost = models.FloatField('成本(RMB)', default=0)
    voltage = models.IntegerField('电压', default=0, choices=VOLTAGE_CHOICES)
    bak = models.TextField('备注', blank=True, max_length=200)

    def __str__(self):
        return "%s(%s)" % (self.cn_name, self.model)

    def weight(self):
        return max([self.net_weight, self.gross_weight, self.volume_weight])
    weight.short_description = '物流重量(KG)'

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


class Category(models.Model):
    parent = models.ForeignKey(
        'self', verbose_name='上级类目', null=True, blank=True)
    name = models.CharField('类目名称', max_length=100)

    def __str__(self):
        return self.slug_name()

    def slug_name(self):
        if self.parent:
            return self.parent.slug_name() + '>' + self.name
        else:
            return self.name

    @classmethod
    def auto_create(cls, cats, parent=None):
        name = cats.pop(0)
        root = cls.objects.filter(name=name, parent=parent)

        if root.exists():
            root = root.get()
        else:
            root = cls(name=name, parent=parent)
            root.save()

        if len(cats) > 0:
            cls.auto_create(cats, parent=root)

    class Meta:
        verbose_name = verbose_name_plural = '产品分类'


class Attr(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='产品详细信息')
    name = models.CharField('属性名', max_length=100)
    value = models.CharField('属性值', max_length=100)

    class Meta:
        verbose_name = verbose_name_plural = '产品属性'


class Extend(models.Model):
    basic = models.ForeignKey('Basic', verbose_name='基本信息')
    category = models.ForeignKey('Category', verbose_name='产品分类')
    # photos = models.CharField('产品图片', max_length=100)
    # attrs = ArrayField(ArrayField(
    #     models.CharField('产品属性', max_length=100, blank=True)))
    port = models.CharField('港口', max_length=100)
    # payment_method = models.IntegerField('付款方式', default=0)
    consignment_term = models.CharField('运输时长', max_length=100)
    packaging_desc = models.TextField('包装描述', max_length=600)

    class Meta:
        verbose_name = verbose_name_plural = '产品详细信息'


class MinOrderQuantity(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='产品详细信息')
    min_order_quantity = models.IntegerField('起订量', default=1)
    min_order_unit = models.IntegerField(
        '起订单位', default=20, choices=UNIT_TYPE_PLURAL)

    class Meta:
        verbose_name = verbose_name_plural = '最小起订量'


class FobPrice(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='产品详细信息')
    money_type = models.IntegerField('货币类型', default=1, choices=CURRENCY_TYPE)
    price_range_min = models.FloatField('最低报价', default=0)
    price_range_max = models.FloatField('最高报价', default=0)
    price_uint = models.IntegerField('报价单位', default=20, choices=UNIT_TYPE)

    class Meta:
        verbose_name = verbose_name_plural = 'FOB报价'


class SupplyAbility(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='产品详细信息')
    supply_quantity = models.IntegerField('产量', max_length=100)
    supply_unit = models.IntegerField(
        '产量单位', default=20, choices=UNIT_TYPE_PLURAL)
    supply_period = models.CharField('产量周期', max_length=20, choices=TIME)


class RichText(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='产品详细信息')
    introduction = models.TextField('产品简介', blank=True)
    specification = models.TextField('参数信息', blank=True)
    application = models.TextField('适用范围', blank=True)
    package = models.TextField('产品包装', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '产品正文信息'
