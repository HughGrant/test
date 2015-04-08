from django.contrib import admin
from django import forms
from django.http import JsonResponse
# from django.utils.safestring import mark_safe
from django.conf.urls import patterns
from . import models
from products.models import Basic
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


class QuotationForm(forms.ModelForm):
    pass


@admin.register(models.Order)
class OrderAdmin(AutoUserAdmin):
    exclude = ('user', )
    inlines = [ProductOrderInline]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = patterns(
            '',
            # url pattern: admin/app_name/model_name/view_name
            # actual url:  admin/buss/order/products_basic/1/
            (r'^products_basic/(?P<basic_id>[0-9]+)/$',
             self.admin_site.admin_view(self.products_basic, cacheable=True))
        )
        return my_urls + urls

    def products_basic(self, request, basic_id):
        b = Basic.objects.get(pk=basic_id)
        return JsonResponse({'cost': b.cost})

    class Media:
        js = ('js/product_order_select_binding.js', )


@admin.register(models.Payment)
class PaymentAdmin(AutoUserAdmin):
    # maybe in the future, this function is only open to manager
    # that would affect the way how this system works

    exclude = ('user', )
    list_display = (
        'sender_info', 'collected_money', 'currency_type', 'exchange_rate',
        'payment_method', 'date', 'verified', 'bak')
    list_editable = (
        'sender_info', 'collected_money', 'currency_type', 'exchange_rate',
        'payment_method', 'bak', 'verified')
