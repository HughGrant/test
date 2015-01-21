from django.contrib import admin
from . import models
from buss.admin import AutoUserAdmin


@admin.register(models.Basic)
class BasicAdmin(AutoUserAdmin):
    exclude = ('user', )
    ordering = ('cn_name', 'model')
    # TODO: using a custom filter
    # Filting products only belongs to this user
    list_filter = ('name', 'cn_name')
    search_fields = ('name', 'cn_name', 'model')
    list_display = ('__str__', 'cost', 'weight', 'size', 'voltage', 'video')


class AttrInline(admin.TabularInline):
    model = models.Attr
    extra = 1


class MinOrderQuantityInline(admin.TabularInline):
    model = models.MinOrderQuantity
    max_num = 1


class SupplyAbilityInline(admin.TabularInline):
    model = models.SupplyAbility
    max_num = 1


class RichTextInline(admin.StackedInline):
    model = models.RichText
    max_num = 1


class FobPriceInline(admin.TabularInline):
    model = models.FobPrice
    max_num = 1


@admin.register(models.Extend)
class ExtendAdmin(admin.ModelAdmin):
    inlines = [
        AttrInline,
        MinOrderQuantityInline,
        FobPriceInline,
        SupplyAbilityInline,
        RichTextInline
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'basic':
            kwargs["queryset"] = models.Basic.objects.filter(user=request.user)

        if db_field.name == 'category':
            kwargs["queryset"] = models.Category.objects.filter(category=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryFilter(admin.SimpleListFilter):
    title = '产品类目'
    parameter_name = 'is_last'

    def lookups(self, request, model_admin):
        return (('is_last', '只显示最终类目'), )

    def queryset(self, request, queryset):
        if self.value() == 'is_last':
            # can be replaced with category__isnull = True
            return queryset.filter(category=None)
        return queryset


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    search_fields = ('name', )
    list_filter = (CategoryFilter, )

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.exclude = ('level', 'parent')
        else:
            self.exclude = ('level', )
        return super().get_form(request, obj, **kwargs)


@admin.register(models.Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'count')
    list_filter = ('name', )
