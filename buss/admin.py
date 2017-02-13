#-*- coding: utf-8 -*-
import io
import time
from django.contrib import admin
from django.http import HttpResponse
import xlsxwriter
from . import models
admin.site.site_header = 'Yason Tech'
admin.site.site_title = 'Yason Tech'
admin.site.index_title = 'Yason Tech'


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
              '折RMB实际收款额', '订单内容', '对应费用', '运费', '净毛利', '跟踪号', '货代公司', '发货日期']
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
    for qs in queryset.order_by('-date'):
        worksheet.write_string(row, 0, qs.date.strftime('%Y/%m/%d'))
        is_old = models.Order.objects.filter(client=qs.client).count()
        if is_old == 1:
            worksheet.write_string(row, 1, '新')
        else:
            worksheet.write_string(row, 1, '老')
        worksheet.write_string(row, 2, qs.client.email)
        worksheet.write_string(row, 3, qs.client.name)
        worksheet.write_string(row, 4, qs.client.country.cn_name)
        # 5, 6
        worksheet.write_formula(row, 7, qs.payments_excel_rmb())
        # 8, 9
        worksheet.write_formula(row, 10, qs.shipping_excel_cost())
        worksheet.write_formula(row, 11, qs.excel_profit())
        worksheet.write_string(row, 12, qs.tracking_number or '无')
        worksheet.write_string(row, 13, qs.logistic_company or '无')
        if qs.ship_date:
            worksheet.write_string(row, 14, qs.ship_date.strftime('%Y/%m/%d'))
        else:
            worksheet.write_string(row, 14, '无')

        # Payment Methods, 5
        next_rows = []
        payment_methods = qs.payments_method()
        if payment_methods:
            next_rows.append(len(payment_methods))
            for index, pm in enumerate(payment_methods, row):
                worksheet.write_string(index, 5, pm)
        else:
            worksheet.write_string(row, 5, "无")

        # Payment Money, 6
        payment_money = qs.payments_collected_money()
        if payment_money:
            next_rows.append(len(payment_money))
            for index, m in enumerate(qs.payments_collected_money(), row):
                worksheet.write_number(index, 6, m)
        else:
            worksheet.write_number(row, 6, 0)

        # product names and quantities, 8 and 9
        name_qty = qs.po_name_qty()
        if name_qty:
            next_rows.append(len(name_qty))
            for index, po_des in enumerate(name_qty, row):
                worksheet.write_string(index, 8, po_des)

            for index, cost in enumerate(qs.prime_excel_cost(), row):
                worksheet.write_formula(index, 9, cost)

        # the extra cost follows unders order description
        extra_costs = qs.extracost_set.count()
        if extra_costs:
            next_rows.append(extra_costs + len(name_qty))
            for index, ec in enumerate(qs.extracost_set.all(), row + len(name_qty)):
                worksheet.write_string(index, 8, ec.discription)
                worksheet.write_number(index, 9, ec.cost)

        row = max(next_rows) + row + 1

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
    ordering = ('-date', )
    search_fields = ('client__name', 'client__email')
    list_filter = ('date', 'ship_date')
    list_display = ('date', 'client_email', 'po_list',
                    'prime_cost_split', 'shipping_cost_split', 'profit')
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
