from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from . import models
from buss.admin import AutoUserAdmin


class DifferentPriceInline(admin.TabularInline):
    model = models.DifferentPrice
    ordering = ('model', 'difference')
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
    search_fields = ('model', 'basic__cn_name')

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['hide_from_index'] = True
        return perms


class AttrInline(admin.TabularInline):
    model = models.Attr
    ordering = ('name', )
    extra = 0


@admin.register(models.Extend)
class ExtendAdmin(AutoUserAdmin):
    inlines = [AttrInline, ]
    raw_id_fields = ('basic', 'different_price')
    exclude = ('user', )
    search_fields = ('basic__cn_name', 'different_price__model')
    list_filter = ordering = ('basic__cn_name', )
    list_display = ('__str__', 'upload_button')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs["queryset"] = models.Category.objects.filter(category=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('js/tinymce/tinymce.min.js', 'js/upload_to_ali.js')


def duplicate_word(modeladmin, req, queryset):
    for qs in queryset:
        qs.count = 0
        qs.title = ''
        qs.model = ''
        qs.id = None
        qs.save()
duplicate_word.short_description = '重复关键字'


@admin.register(models.TitleKeyword)
class TitleKeywordAdmin(AutoUserAdmin):
    exclude = ('user', 'count')
    search_fields = ('word', 'title')
    list_filter = ordering = ('model', )
    list_editable = ('title', 'model', 'word', 'count')
    list_display = ('list_link', 'word', 'title', 'model', 'count')
    list_display_links = ('list_link', )
    actions = [duplicate_word, ]


@admin.register(models.QuotationTemplate)
class QuotationTemplateAdmin(AutoUserAdmin):
    exclude = ('user', )
    raw_id_fields = ('dp', )
    search_fields = ('dp__model', )
    list_filter = ordering = ('dp__model', )
    list_display = ('show_model', 'copy_link')


@admin.register(models.Trace)
class TraceAdmin(AutoUserAdmin):
    exclude = ('user', )
    search_fields = ('model', 'twk__title')
    list_filter = ('model', 'le__email')
    list_display = ('title', 'model', 'email', 'update_time', 'link')
