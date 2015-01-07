from django.contrib import admin
from products.models import Basic, Keyword, Category
from buss.admin import AutoUserAdmin


@admin.register(Basic)
class BasicAdmin(AutoUserAdmin):
    exclude = ('user', )
    list_filter = ('name', 'cn_name')
    search_fields = ('name', 'cn_name', 'model')
    list_display = ('__str__', 'cost', 'weight', 'size', 'voltage', 'video')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'count')
    list_filter = ('name', )


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


@admin.register(Category)
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
