from django.db import models
from django.contrib.auth.models import User
from preset import *
from clients.models import LoginEmail


class Basic(models.Model):
    user = models.ForeignKey(User)
    cn_name = models.CharField('中文名', blank=True, max_length=200)
    bak = models.TextField('备注', blank=True, max_length=200)

    def __str__(self):
        return self.cn_name

    def price(self):
        qs = DifferentPrice.objects.filter(basic_id=self.id)
        if not qs.exists():
            return '未设置: 0 RMB, 0KG, 0*0*0CM'
        qs = qs.order_by('model', 'difference')
        fs = '<br><br>'.join([dp.description() for dp in qs.all()])
        return fs
    price.short_description = '报价'
    price.allow_tags = True

    def spare_parts(self):
        qs = Accessory.objects.filter(basic_id=self.id)
        if not qs.exists():
            return ''
        # qs = qs.order_by('model', 'difference')
        fs = '<br><br>'.join([dp.description() for dp in qs.all()])
        return fs
    spare_parts.short_description = '配件'
    spare_parts.allow_tags = True

    class Meta:
        verbose_name = verbose_name_plural = '基本信息'


class QuotationTemplate(models.Model):
    user = models.ForeignKey(User)
    dp = models.ForeignKey('DifferentPrice', null=True, verbose_name='产品')
    content = models.TextField('正文', blank=True, max_length=100000)

    def copy_link(self):
        return '拷贝模板'
    copy_link.short_description = '动作'
    copy_link.allow_tags = True

    def show_model(self):
        return self.dp.__str__()
    show_model.short_description = '产品型号'

    class Meta:
        verbose_name = verbose_name_plural = '报价模板'


class TitleKeyword(models.Model):
    user = models.ForeignKey(User)
    model = models.CharField('型号', max_length=200, default="")
    title = models.CharField('标题', max_length=200, blank=True, default="")
    word = models.CharField('内容', max_length=200, default="")
    count = models.IntegerField('计数', default=0)

    @classmethod
    def get_pair(cls, model):
        tk = cls.objects.filter(model=model).exclude(title="")
        if tk.exists():
            return tk.order_by('count')[:1].get()
        return None

    def count_plus(self):
        self.count += 1
        self.save()

    def list_link(self):
        return self.word
    list_link.short_description = '链接'

    def __str__(self):
        return "%s-%s" % (self.word, self.count)

    class Meta:
        unique_together = ('model', 'word')
        verbose_name = verbose_name_plural = '更新数据'


class Trace(models.Model):
    user = models.ForeignKey(User)
    tkw = models.ForeignKey('TitleKeyword', verbose_name='标题与关键字')
    # login email information
    le = models.ForeignKey(LoginEmail, verbose_name='帐户信息', null=True)
    # alibaba product id
    apid = models.IntegerField('阿里产品ID', default=0)
    update_time = models.DateTimeField('最后更新时间', auto_now_add=True)

    @classmethod
    def tracing(cls, **kwargs):
        le = kwargs['le']
        apid = kwargs['apid']
        twk = kwargs['tkw']
        user = kwargs['user']

        t = cls.objects.filter(le=le, apid=apid, user=user)
        if t.exists():
            t = t.get()
            t.twk = twk
            t.save()
        else:
            t = cls(**kwargs)
            t.save()

    def title(self):
        return self.tkw.title
    title.short_description = '标题'

    def email(self):
        return self.le.email
    email.short_description = '对应邮箱帐号'

    def modelx(self):
        return self.tkw.model
    modelx.short_description = '产品型号'

    def link(self):
        l = "http://hz-productposting.alibaba.com/product/editing.htm?id=%d" % self.apid
        return '<a target="blank" href="%s">点击更新</a>' % l
    link.short_description = '更新链接'
    link.allow_tags = True

    class Meta:
        unique_together = ('tkw', 'apid')
        verbose_name = verbose_name_plural = '更新记录'


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
    basic = models.ForeignKey('Basic', verbose_name='基本信息')
    difference = models.CharField('描述', max_length=100)
    price = models.FloatField('价钱(RMB)', default=0)

    def __str__(self):
        return '%s: %s' % (self.difference, self.price)

    def description(self):
        return '%s: %sRMB' % (self.difference, self.price)

    class Meta:
        verbose_name = verbose_name_plural = '产品配件'


class DifferentPrice(models.Model):
    basic = models.ForeignKey('Basic', verbose_name='基本信息')
    model = models.CharField('型号', blank=True, max_length=200)
    difference = models.CharField('描述', max_length=100)
    price = models.FloatField('成本(RMB)', default=0)
    profit = models.FloatField('利润', default=0)
    video = models.CharField('视频', blank=True, max_length=200)
    size = models.CharField('尺寸(CM)', blank=True, max_length=200)
    weight = models.FloatField('积重(KG)', default=0)

    def __str__(self):
        return '%s(%s)-%s: %s' % (
            self.basic.cn_name, self.model, self.difference, self.price)

    def min_profit(self):
        if self.profit:
            return round((self.price + self.profit) / 6)
        return 0

    def max_profit(self):
        if self.profit:
            return round((self.price + self.profit) * 1.1 / 6)
        return 0

    def description(self):
        return '%s-%s: %sRMB, %sKG, %sCM' % (
            self.model, self.difference, self.price, self.weight, self.size)

    class Meta:
        verbose_name = verbose_name_plural = '差异价'


class Attr(models.Model):
    extend = models.ForeignKey('Extend', verbose_name='详细信息')
    name = models.CharField('属性名', max_length=100)
    value = models.CharField('属性值', max_length=200)

    def __str__(self):
        return '%s: %s' % (self.name, self.value)

    class Meta:
        verbose_name = verbose_name_plural = '属性'


class Extend(models.Model):
    basic = models.ForeignKey('Basic', null=True, verbose_name='基本信息')
    different_price = models.ForeignKey(
        'DifferentPrice', null=True, verbose_name='差异价')
    user = models.ForeignKey(User)
    category = models.ForeignKey('Category', verbose_name='分类')
    moq = models.ForeignKey('MOQ', verbose_name='最小起订量')
    supply_ability = models.ForeignKey('SupplyAbility', verbose_name='供贷能力')
    content = models.TextField('正文', blank=True, max_length=100000)
    # the following attr are fixed by default value
    # port, payment_terms, consignment_term, packaging_desc

    def __str__(self):
        return self.different_price.__str__()

    def upload_button(self):
        if self.different_price is None:
            return ''
        return '<button id="%s" class="ali_u" model="%s">上传</button>' % (
                self.id, self.different_price.model)

    upload_button.allow_tags = True
    upload_button.short_description = '动作'

    class Meta:
        verbose_name = verbose_name_plural = '详细信息'


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
