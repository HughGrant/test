from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from preset import *


class Basic(models.Model):
    cn_name = models.CharField('中文名', blank=True, max_length=200)
    name = models.CharField('英文名', blank=True, max_length=200)
    model = models.CharField('型号', blank=True, max_length=200)
    keyword = models.CharField('默认主关键字', blank=True, max_length=200)
    video = models.CharField('视频', blank=True, max_length=200)
    bak = models.TextField('备注', blank=True, max_length=200)

    def __str__(self):
        if self.cn_name:
            return "%s(%s)" % (self.cn_name, self.model)
        else:
            return "%s(%s)" % (self.name, self.model)

    def price(self):
        qs = DifferentPrice.objects.filter(basic_id=self.id)
        if not qs.exists():
            return '未设置: 0 RMB, 0KG, 0*0*0CM'
        fs = '<br><br>'.join([dp.description() for dp in qs.all()])
        return format_html(fs)
    price.short_description = '报价'
    price.allow_tabs = True

    def has_accessory(self):
        return Accessory.objects.filter(basic_id=self.id).exists()
    has_accessory.short_description = '配件'
    has_accessory.boolean = True

    def has_video(self):
        return self.video != ''
    has_video.short_description = '视频'
    has_video.boolean = True

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
    ali_id = models.IntegerField('阿里ID', default=0)

    def __str__(self):
        return self.slug_name()

    def slug_name(self):
        if self.parent:
            return self.parent.slug_name() + '>' + self.name
        else:
            return self.name

    def has_ali_id(self):
        return self.ali_id != 0
    has_ali_id.short_description = '是否已添加阿里ID'
    has_ali_id.boolean = True

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
            return cls.auto_create(cats, parent=root)
        else:
            return root

    class Meta:
        verbose_name = verbose_name_plural = '产品分类'


class Accessory(models.Model):
    basic = models.ForeignKey('Basic', verbose_name='产品基本信息')
    difference = models.CharField('描述', max_length=100)
    price = models.FloatField('价钱(RMB)', default=0)

    def __str__(self):
        return '%s: %s' % (self.difference, self.price)

    class Meta:
        verbose_name = verbose_name_plural = '产品配件'


class DifferentPrice(models.Model):
    basic = models.ForeignKey('Basic', verbose_name='产品基本信息')
    difference = models.CharField('描述', max_length=100)
    price = models.FloatField('价钱(RMB)', default=0)
    size = models.CharField('尺寸(CM)', blank=True, max_length=200)
    net_weight = models.FloatField('净重(KG)', default=0)
    gross_weight = models.FloatField('毛重(KG)', default=0)
    volume_weight = models.FloatField('积重(KG)', default=0)

    def __str__(self):
        return '%s-%s: %s' % (
            self.basic.cn_name, self.difference, self.price)

    def weight(self):
        return max([self.net_weight, self.gross_weight, self.volume_weight])

    def description(self):
        return '%s: %sRMB, %sKG, %sCM' % (
            self.difference, self.price, self.weight(), self.size)

    class Meta:
        verbose_name = verbose_name_plural = '产品差异价'


class Attr(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='产品详细信息')
    name = models.CharField('属性名', max_length=100)
    value = models.CharField('属性值', max_length=200)

    def __str__(self):
        return '%s: %s' % (self.name, self.value)

    class Meta:
        verbose_name = verbose_name_plural = '产品属性'


class Picture(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='产品详细信息')
    url = models.CharField('图片来源', max_length=300)

    class Meta:
        verbose_name = verbose_name_plural = '产品图片'


class Extend(models.Model):
    basic = models.ForeignKey('Basic', null=True, verbose_name='基本信息')
    user = models.ForeignKey(User)
    title = models.CharField('标题', blank=True, max_length=200)
    category = models.ForeignKey('Category', verbose_name='产品分类')
    moq = models.ForeignKey(
        'MOQ', verbose_name='最小起订量')
    fob_price = models.ForeignKey('FobPrice', verbose_name='FOB报价')
    port = models.CharField('港口', max_length=100)
    payment_terms = models.CharField('付款方式', max_length=200)
    supply_ability = models.ForeignKey('SupplyAbility', verbose_name='供贷能力')
    packaging_desc = models.CharField('包装描述', max_length=600)
    consignment_term = models.CharField('运输时长', max_length=100)
    rich_text = models.TextField('产品正文', blank=True, max_length=100000)
    upload_count = models.IntegerField('已上传次数', default=0)

    def __str__(self):
        if not self.title:
            return self.basic.__str__()
        return self.title

    def upload_button(self):
        return format_html(
            '<button id="{0}" class="ali_upload">上传</button>',
            self.id)
    upload_button.allow_tabs = True
    upload_button.short_description = '动作'

    def has_rich_text(self):
        return self.rich_text != ''
    has_rich_text.boolean = True
    has_rich_text.short_description = '产品正文'

    class Meta:
        verbose_name = verbose_name_plural = '产品详细信息'


class MOQ(models.Model):
    min_order_quantity = models.IntegerField('起订量', default=1)
    min_order_unit = models.IntegerField(
        '起订单位', default=20, choices=UNIT_TYPE_PLURAL)

    def __str__(self):
        return '%s %s' % (
            self.min_order_quantity,
            self.get_min_order_unit_display())

    class Meta:
        unique_together = ('min_order_quantity', 'min_order_unit')
        verbose_name = verbose_name_plural = '最小起订量'


class FobPrice(models.Model):
    money_type = models.IntegerField('货币类型', default=1, choices=CURRENCY_TYPE)
    price_range_min = models.FloatField('最低报价', default=0)
    price_range_max = models.FloatField('最高报价', default=0)
    price_unit = models.IntegerField('报价单位', default=20, choices=UNIT_TYPE)

    def __str__(self):
        return '%s %s-%s %s' % (
            self.get_money_type_display(),
            self.price_range_min,
            self.price_range_max,
            self.get_price_unit_display())

    class Meta:
        unique_together = (
            'money_type',
            'price_range_min',
            'price_range_max',
            'price_unit')
        verbose_name = verbose_name_plural = 'FOB报价'


class SupplyAbility(models.Model):
    supply_quantity = models.IntegerField('产量', default=0)
    supply_unit = models.IntegerField(
        '产量单位', default=20, choices=UNIT_TYPE_PLURAL)
    supply_period = models.CharField('产量周期', max_length=20, choices=TIME)

    def __str__(self):
        return '%s %s per %s' % (
            self.supply_quantity,
            self.get_supply_unit_display(),
            self.get_supply_period_display())

    class Meta:
        unique_together = (
            'supply_quantity', 'supply_unit', 'supply_period')
        verbose_name = verbose_name_plural = '供贷能力'
