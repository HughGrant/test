from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from . import models
from buss.admin import AutoUserAdmin


class DifferentPriceInline(admin.TabularInline):
    model = models.DifferentPrice
    extra = 0


class AccesscoryInline(admin.TabularInline):
    model = models.Accessory
    extra = 0


@admin.register(models.Basic)
class BasicAdmin(AutoUserAdmin):
    inlines = [
        DifferentPriceInline,
        AccesscoryInline
    ]
    exclude = ('user', )
    ordering = list_filter = search_fields = ('cn_name', )
    list_display = ('__str__', 'price')


class MOQForm(forms.ModelForm):

    def clean(self):
        if models.MOQ.objects.filter(**self.cleaned_data).exists():
            raise ValidationError('已存在，无需重复创建')

    class Meta:
        fields = ('min_order_quantity', 'min_order_unit')
        model = models.MOQ


@admin.register(models.MOQ)
class MOQAdmin(admin.ModelAdmin):
    form = MOQForm

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['hide_from_index'] = True
        return perms


class SPForm(forms.ModelForm):

    def clean(self):
        if models.SupplyAbility.objects.filter(**self.cleaned_data).exists():
            raise ValidationError('已存在，无需重复创建')

    class Meta:
        fields = (
            'supply_quantity', 'supply_unit', 'supply_period')
        model = models.SupplyAbility


@admin.register(models.SupplyAbility)
class SupplyAbilityAdmin(admin.ModelAdmin):
    form = SPForm

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['hide_from_index'] = True
        return perms


@admin.register(models.DifferentPrice)
class DifferentPriceAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['hide_from_index'] = True
        return perms


class AttrInline(admin.TabularInline):
    model = models.Attr
    ordering = ('name', )
    extra = 0


class TitleInline(admin.TabularInline):
    model = models.Title
    extra = 0


@admin.register(models.Extend)
class ExtendAdmin(AutoUserAdmin):
    inlines = [
        TitleInline,
        AttrInline
    ]
    raw_id_fields = ('basic', 'different_price')
    exclude = ('user', )
    search_fields = list_filter = ordering = ('basic__cn_name', )
    list_display = ('__str__', 'upload_button')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs["queryset"] = models.Category.objects.filter(category=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('js/tinymce/tinymce.min.js', 'js/upload_to_ali.js')


# class CategoryFilter(admin.SimpleListFilter):
#     title = '产品类目'
#     parameter_name = 'is_last'

#     def lookups(self, request, model_admin):
#         return (('is_last', '只显示最终类目'), )

#     def queryset(self, request, queryset):
#         if self.value() == 'is_last':
#             # can be replaced with category__isnull = True
#             return queryset.filter(category=None)
#         return queryset


# @admin.register(models.Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'has_ali_id')
#     readonly_fields = ('name', )
#     search_fields = ('name', )
#     list_filter = (CategoryFilter, )

#     def get_form(self, request, obj=None, **kwargs):
#         if obj:
#             self.exclude = ('level', 'parent')
#         else:
#             self.exclude = ('level', )
#         return super().get_form(request, obj, **kwargs)