from django.db import models
from django.contrib.auth.models import User
from clients.models import Client
from products.models import Basic
from preset import CURRENCY_TYPE, PAYMENT_METHOD


class Order(models.Model):
    user = models.ForeignKey(User)
    client = models.ForeignKey(
        Client, blank=True, null=True, verbose_name='客户')
    payment = models.ForeignKey(
        'Payment', blank=True, null=True, verbose_name='付款信息')
    total_cost = models.FloatField('总成本', default=0)
    shipping_cost = models.FloatField('总运费', default=0)
    total_price = models.FloatField('总报价', default=0)
    bak = models.TextField('备注', blank=True, max_length=500)
    date = models.DateField('日期', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '定单'
    # def profit(self):
    #     if self.payment.currency_type == 'CH':
    #         rmb = self.payment.collected_money
    #     else:
    #         rmb = self.payment.collected_money * self.payment.exchange_rate
    #     return rmb - self.total_cost - self.shipping_cost


class ProductOrder(models.Model):
    order = models.ForeignKey('Order')
    product = models.ForeignKey(Basic, verbose_name='产品')
    quantity = models.IntegerField('数量', default=0)
    cost = models.FloatField('成本', default=0)
    price = models.FloatField('单价', default=0)
    bak = models.CharField('备注', blank=True, max_length=200)

    class Meta:
        verbose_name = verbose_name_plural = '定单内容'


class Payment(models.Model):
    user = models.ForeignKey(User)
    sender_info = models.CharField('付款人信息', blank=True, max_length=100)
    collected_money = models.FloatField('收款金额', default=0)
    currency_type = models.IntegerField(
        '货币类型', default=1, choices=CURRENCY_TYPE)
    exchange_rate = models.FloatField('对人民币汇率', default=6.2)
    payment_method = models.IntegerField(
        '付款方式', default=1, choices=PAYMENT_METHOD)
    verified = models.BooleanField('是否已核实付款', default=False)
    date = models.DateField('日期', auto_now_add=True)
    bak = models.CharField('备注', blank=True, max_length=200)

    class Meta:
        verbose_name = verbose_name_plural = '付款信息'

    def __str__(self):
        return '%s(%s%s)' % (
            self.sender_info, self.collected_money, self.currency_type)

# class PaymentIssue(models.Model):
#     payment = models.ForeignKey('Payment', verbose_name='付款信息')
#     creator = models.ForeignKey(User, verbose_name='创建者', related_name='+')
#     user = models.ForeignKey(User, verbose_name='所属人')
#     issue = models.TextField('纠纷内容', max_length=1000)
#     date = models.DateField('日期', auto_now_add=True)
#     handled = models.BooleanField('是还已处理', default=False)
#     handle_date = models.DateField('处理日期', null=True)

#     class Meta:
#         verbose_name = verbose_name_plural = '纠纷'
