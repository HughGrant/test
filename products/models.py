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

# {name: 'name', title:'产品名'},
# {name: 'keywords', title:'关键字'},
# {name: 'category', title:'类目'},
# {name: 'summary', title:'概览'},
# {name: 'photos', title:'产品图片'},
# {name: 'attrs', title:'产品属性'},
# {name: 'min_order_quantity', title:'起订量'},
# {name: 'min_order_unit', title:'起订单位'},
# {name: 'money_type', title:'货币类型'},
# {name: 'price_range_min', title:'最低报价'},
# {name: 'price_range_max', title:'最高报价'},
# {name: 'price_uint', title:'报价单位'},
# {name: 'port', title:'港口'},
# {name: 'payment_method', title:'付款方式'},
# {name: 'supply_quantity', title:'产量'},
# {name: 'supply_unit', title:'产量单位'},
# {name: 'supply_period', title:'产量周期'},
# {name: 'consignment_term', title:'运输时长'},
# {name: 'packaging_desc', title:'包装描述'},
# {name: 'rich_text', title:'产品正文'},