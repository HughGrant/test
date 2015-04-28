import io, time
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
        return super().get_queryset(request).filter(user=request.user)


class ProductOrderInline(admin.TabularInline):
    model = models.ProductOrder
    extra = 1


class PaymentInline(admin.TabularInline):
    model = models.Payment
    extra = 1
    exclude = ('user', )


def make_month_profit(modeladmin, req, queryset):
    titles = ['日期', '客户性质', '客户邮箱地址', '客户名字', '国家', '收款金额(USD)', '付款方式',
              '折RMB实际收款额', '商品名称及数量及单价', '货物成本', '运费', '净毛利', '跟踪号',
              '货代公司', '发货日期']
    excel_file = io.BytesIO()
    file_name = '%s.xlsx' % (time.strftime('%Y-%m-%d'))
    workbook = xlsxwriter.Workbook(excel_file, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    # write the titles first
    bold = workbook.add_format({'bold': True})
    text_wrap = workbook.add_format({'text_wrap': True})
    for col, title in enumerate(titles):
        worksheet.write(0, col, title, bold)
    # filling the data
    row = 1
    for qs in queryset:
        row_t = (row + 1, row + 1, row + 1)
        worksheet.write_string(row, 0, qs.date.strftime('%Y-%m-%d'))
        is_old = models.Order.objects.filter(client=qs.client).count()
        if is_old == 1:
            worksheet.write_string(row, 1, '新')
        else:
            worksheet.write_string(row, 1, '老')
        worksheet.write_string(row, 2, qs.client.email)
        worksheet.write_string(row, 3, qs.client.name)
        worksheet.write_string(row, 4, qs.client.country.cn_name)
        worksheet.write_number(row, 5, qs.payments_money())
        worksheet.write_string(row, 6, qs.payments_method())
        worksheet.write_number(row, 7, qs.payments_rmb())
        worksheet.write(row, 8, qs.po_excel_str(), text_wrap)
        worksheet.write_number(row, 9, qs.prime_cost())
        worksheet.write_number(row, 10, qs.shipping_cost())
        worksheet.write_formula(row, 11, '=H%d-J%d-K%d' % row_t)
        row += 1

    worksheet.set_column('A:A', 12)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('D:D', 17)
    worksheet.set_column('F:F', 17)
    worksheet.set_column('H:H', 17)
    worksheet.set_column('I:I', 30)
    workbook.close()
    ct = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    resp = HttpResponse(excel_file.getvalue())
    resp['Content-Disposition'] = 'attachment; filename=%s' % file_name
    resp['Content-type'] = ct
    return resp
make_month_profit.short_description = '生成利润表'


@admin.register(models.Order)
class OrderAdmin(AutoUserAdmin):
    exclude = ('user', )
    search_fields = ('client', )
    list_filter = ('date', )
    list_display = ('client', 'payments_rmb', 'po_list', 'prime_cost',
                    'shipping_cost', 'profit', 'date', 'bak')
    inlines = [ProductOrderInline, PaymentInline]
    actions = [make_month_profit]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    exclude = ('user', )
    list_filter = ('date', )
    search_fields = ('sender_info', )
    list_display = (
        'sender_info', 'collected_money', 'currency_type', 'exchange_rate',
        'payment_method', 'rmb', 'date', 'bak')

    def get_queryset(self, req):
        return super().get_queryset(req).filter(order__user=req.user)
