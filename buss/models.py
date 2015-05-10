from django.db import models
from django.contrib.auth.models import User
from clients.models import Client
from products.models import DifferentPrice
from preset import CURRENCY_TYPE, PAYMENT_METHOD


class Order(models.Model):
    user = models.ForeignKey(User)
    client = models.ForeignKey(
        Client, blank=True, null=True, verbose_name='客户')
    tracking_number = models.CharField('跟踪号', blank=True, max_length=200)
    logistic_company = models.CharField('货代公司', blank=True, max_length=200)
    date = models.DateTimeField('创建日期', auto_now=True)
    ship_date = models.DateField('发贷日期', null=True)
    bak = models.TextField('备注', blank=True, max_length=500)

    def po_excel_str(self):
        descriptions = []
        for po in self.productorder_set.all():
            descriptions.append(po.description())
        return '\n'.join(descriptions)

    def po_list(self):
        descriptions = []
        for po in self.productorder_set.all():
            descriptions.append(po.description())
        return '<br><br>'.join(descriptions)
    po_list.short_description = '定单内容'
    po_list.allow_tags = True

    def profit(self):
        return self.payments_rmb() - self.prime_cost() - self.shipping_cost()
    profit.short_description = '净毛利(RMB)'

    def payments_rmb(self):
        rmb = 0
        for payment in self.payment_set.all():
            rmb += payment.rmb()
        return rmb
    payments_rmb.short_description = '实际收款额(RMB)'

    def payments_excel_money(self):
        usd = []
        for payment in self.payment_set.all():
            usd.append(str(payment.collected_money))
        return '=' + '+'.join(usd)

    def payments_excel_rmb(self):
        rmb = []
        for payment in self.payment_set.all():
            rmb.append(payment.excel_rmb())
        return '=' + '+'.join(rmb)

    def payments_method(self):
        methods = []
        for payment in self.payment_set.all():
            methods.append(payment.get_payment_method_display())
        return ','.join(set(methods))

    def prime_cost(self):
        cost = 0
        for po in self.productorder_set.all():
            cost += po.prime_cost()
        return cost
    prime_cost.short_description = '贷物成本(RMB)'

    def prime_excel_cost(self):
        cost = []
        for po in self.productorder_set.all():
            cost.append('%d*%d' % (po.product.price, po.quantity))
        return '=' + '+'.join(cost)

    def shipping_cost(self):
        cost = 0
        for po in self.productorder_set.all():
            cost += po.shipping_cost
        return cost
    shipping_cost.short_description = '运费(RMB)'

    def shipping_excel_cost(self):
        cost = []
        for po in self.productorder_set.all():
            cost.append(str(po.shipping_cost))
        return '=' + '+'.join(cost)

    def __str__(self):
        return '%s-定单ID:%s' % (self.client.__str__(), self.id)

    class Meta:
        verbose_name = verbose_name_plural = '定单'


class ProductOrder(models.Model):
    order = models.ForeignKey('Order')
    product = models.ForeignKey(DifferentPrice, verbose_name='产品价格')
    quantity = models.IntegerField('数量', default=1)
    shipping_cost = models.FloatField('运费', default=0)

    def __str__(self):
        return self.product.__str__()

    def description(self):
        return '%s-%s * %s' % (
            self.product.basic.cn_name, self.product.difference, self.quantity)

    def prime_cost(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = verbose_name_plural = '定单内容'


class Payment(models.Model):
    order = models.ForeignKey('Order', verbose_name='定单')
    sender_info = models.CharField('付款人信息', max_length=100)
    collected_money = models.FloatField('收款金额', default=0)
    currency_type = models.IntegerField(
        '货币类型', default=1, choices=CURRENCY_TYPE)
    exchange_rate = models.FloatField('对人民币汇率', default=6.2)
    payment_method = models.IntegerField(
        '付款方式', default=1, choices=PAYMENT_METHOD)
    date = models.DateField('日期')

    class Meta:
        verbose_name = verbose_name_plural = '付款信息'

    def rmb(self):
        if self.payment_method == 1:
            return self.collected_money / 1.04 * self.exchange_rate
        return self.collected_money * self.exchange_rate
    rmb.short_description = '折RMB实际收款额'

    def excel_rmb(self):
        if self.payment_method == 1:
            return '%f/1.04*%f' % (self.collected_money, self.exchange_rate)
        return '%f*%f' % (self.collected_money, self.exchange_rate)

    def __str__(self):
        return '%s(%s%s %s)' % (
            self.sender_info,
            self.collected_money,
            self.get_currency_type_display(),
            self.get_payment_method_display())

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
