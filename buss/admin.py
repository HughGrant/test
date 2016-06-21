#-*- coding: utf-8 -*-
import io
import time
from django.contrib import admin
from django.http import HttpResponse
import xlsxwriter
from . import models
admin.site.site_header = '亚新科技'
admin.site.site_title = 'Yason Tech'
admin.site.index_title = '亚新电子科技有限公司'


class AutoUserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        return super(AutoUserAdmin, self).get_queryset(request).filter(user=request.user)


class ProductOrderInline(admin.TabularInline):
    model = models.ProductOrder
    raw_id_fields = ('product', )
    extra = 0


class ExtraCostInline(admin.TabularInline):
    model = models.ExtraCost
    extra = 0


class PaymentInline(admin.TabularInline):
    model = models.Payment
    extra = 0
    exclude = ('user', )


def make_month_profit(modeladmin, req, queryset):
    titles = ['日期', '客户性质', '客户邮箱地址', '客户名字', '国家', '付款方式', '收款金额(USD)',
              '折RMB实际收款额', '商品名称及数量及单价', '货物成本', '运费', '净毛利', '跟踪号',
              '货代公司', '发货日期']
    excel_file = io.BytesIO()
    workbook = xlsxwriter.Workbook(excel_file, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    # write the titles first
    title_format = workbook.add_format({'bold': True, 'align': 'center'})
    po_format = workbook.add_format({'text_wrap': True, 'align': 'center'})
    for col, title in enumerate(titles):
        worksheet.write(0, col, title, title_format)
    # filling the data
    row = 1
    for qs in queryset.order_by('date'):
        worksheet.write_string(row, 0, qs.date.strftime('%Y/%m/%d'))
        is_old = models.Order.objects.filter(client=qs.client).count()
        if is_old == 1:
            worksheet.write_string(row, 1, '新')
        else:
            worksheet.write_string(row, 1, '老')
        worksheet.write_string(row, 2, qs.client.email)
        worksheet.write_string(row, 3, qs.client.name)
        worksheet.write_string(row, 4, qs.client.country.cn_name)
        worksheet.write_formula(row, 7, qs.payments_excel_rmb())

        worksheet.write_formula(row, 10, qs.shipping_excel_cost())
        worksheet.write_formula(row, 11, qs.excel_profit())
        worksheet.write_string(row, 12, qs.tracking_number)
        worksheet.write_string(row, 13, qs.logistic_company)
        worksheet.write_string(row, 14, qs.ship_date.strftime('%Y/%m/%d'))

        max_iters = []
        # Payment Methods
        for index, pm in enumerate(qs.payments_method(), row):
            worksheet.write_string(index, 5, pm)
        max_iters.append(index)

        # Payment Money
        for index, m in enumerate(qs.payments_collected_money(), row):
            worksheet.write_number(index, 6, m)
        max_iters.append(index)

        # product names and quantities
        name_qty = qs.po_name_qty()
        max_po = len(name_qty)

        for index, po_des in enumerate(name_qty, row):
            worksheet.write_string(index, 8, po_des)

        for index, cost in enumerate(qs.prime_excel_cost(), row):
            worksheet.write_formula(index, 9, cost)

        # the extra cost follows unders order description
        for index, ec in enumerate(qs.extracost_set.all(), max_po + 1):
            worksheet.write_string(index, 8, ec.discription)
            worksheet.write_number(index, 9, ec.cost)
        max_iters.append(index)

        row = max(max_iters) + 2

    # total profit sum
    worksheet.write_string(row, 10, '总利润')
    worksheet.write_formula(row, 11, 'SUM(L2:L%d)' % row)

    # style
    center_algin = workbook.add_format({'align': 'center'})
    worksheet.set_column('A:O', 15, center_algin)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('H:H', 25)
    worksheet.set_column('I:I', 35)
    workbook.close()
    ct = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    resp = HttpResponse(excel_file.getvalue())
    file_name = '%s.xlsx' % (time.strftime('%Y-%m-%d'))
    resp['Content-Disposition'] = 'attachment; filename=%s' % file_name
    resp['Content-type'] = ct
    return resp
make_month_profit.short_description = '生成利润表'


@admin.register(models.Order)
class OrderAdmin(AutoUserAdmin):
    exclude = ('user', )
    search_fields = ('client__name', 'client__email')
    list_filter = ordering = ('date', 'ship_date')
    list_display = ('date', 'client_email', 'payments_rmb_short', 'po_list',
                    'prime_cost_split', 'shipping_cost', 'profit', 'logistic',
                    'ship_date')
    raw_id_fields = ('client', )
    inlines = [PaymentInline, ProductOrderInline, ExtraCostInline]
    actions = [make_month_profit, ]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    exclude = ('user', 'order')
    list_filter = ('date', )
    search_fields = ('sender_info', )
    list_display = (
        'date', 'sender_info', 'collected_money', 'currency_type',
        'exchange_rate', 'payment_method', 'rmb')

    def get_queryset(self, req):
        return super(PaymentAdmin, self).get_queryset(req).filter(order__user=req.user)
