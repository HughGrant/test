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


@admin.register(models.MOQ)
class MOQAdmin(AutoUserAdmin):
    exclude = ('user', )

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['hide_from_index'] = True
        return perms


@admin.register(models.SupplyAbility)
class SupplyAbilityAdmin(AutoUserAdmin):
    exclude = ('user', )

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['hide_from_index'] = True
        return perms


@admin.register(models.FobPrice)
class FobPriceAdmin(AutoUserAdmin):
    exclude = ('user', )

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['hide_from_index'] = True
        return perms


class AttrInline(admin.TabularInline):
    model = models.Attr
    extra = 1


class PictureInline(admin.TabularInline):
    model = models.Picture
    extra = 1


@admin.register(models.Extend)
class ExtendAdmin(admin.ModelAdmin):
    inlines = [
        AttrInline,
        PictureInline
    ]
    list_display = ('__str__', 'upload_button')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'basic':
            kwargs["queryset"] = models.Basic.objects.filter(user=request.user)

        if db_field.name == 'category':
            kwargs["queryset"] = models.Category.objects.filter(category=None)

        if db_field.name == 'fob_price':
            kwargs["queryset"] = models.FobPrice.objects.filter(
                user=request.user)

        if db_field.name == 'moq':
            kwargs["queryset"] = models.MOQ.objects.filter(user=request.user)

        if db_field.name == 'supply_ability':
            kwargs["queryset"] = models.SupplyAbility.objects.filter(
                user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('js/upload_to_ali.js', )


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
