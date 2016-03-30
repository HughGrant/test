from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term == '':
            return queryset, use_distinct
        qs = models.DifferentPrice.objects.filter(model__icontains=search_term)
        if qs.count == 0:
            return qs, use_distinct

        ids = qs.values_list('basic_id', flat=True).distinct()
        qs = models.Basic.objects.filter(id=ids)
        return qs, use_distinct


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


class TKWFilter(admin.SimpleListFilter):
    title = '产品型号'
    parameter_name = 'model'

    def lookups(self, request, model_admin):
        # returns a tuple
        pairs = []
        names = models.TitleKeyword.objects.values_list('model').distinct()
        for n in names:
            r = models.TitleKeyword.objects.filter(model=n[0])
            total = r.count()
            used = r.aggregate(Sum('count'))['count__sum']
            pairs.append((n[0], "%s (%d-%d)" % (n[0], used, total)))
        return pairs

    def queryset(self, request, queryset):
        # self.value() represents the filter value
        if self.value():
            return queryset.filter(model=self.value())
        return queryset


@admin.register(models.TitleKeyword)
class TitleKeywordAdmin(AutoUserAdmin):
    exclude = ('user', 'count')
    search_fields = ('word', 'title')
    list_filter = (TKWFilter, )
    ordering = ('model', )
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
    search_fields = ('apid', )
    list_filter = ('le__email', )
    list_display = ('title', 'modelx', 'apid', 'email', 'update_time', 'link')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term == '':
            return queryset, use_distinct
        if search_term.isnumeric():
            return queryset, use_distinct
        qs = models.TitleKeyword.objects.filter(model=search_term)
        if qs.count == 0:
            return queryset, use_distinct

        ids = qs.values_list('id', flat=True)
        qs = models.Trace.objects.filter(tkw__in=ids)
        return qs, use_distinct
