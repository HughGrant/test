from django.contrib import admin
from buss.admin import AutoUserAdmin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ('cn_name', 'en_name', 'code')
    list_display = ('cn_name', 'en_name', 'code', 'voltage', 'socket')
    # readonly_fields = ('ibt_id', 'cn_name', 'en_name', 'code')
    list_filter = ('voltage', 'socket')


class AddressInline(admin.StackedInline):
    model = models.Address
    raw_id_fields = ('country', )
    extra = 0


class ClientCountryFilter(admin.SimpleListFilter):
    title = '国家'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        # returns a tuple
        names = models.Client.objects.values_list(
            'country__id', 'country__cn_name').distinct()
        return names

    def queryset(self, request, queryset):
        # self.value() represents the filter value
        if self.value():
            return queryset.filter(country__id=self.value())
        return queryset


@admin.register(models.Client)
class ClientAdmin(AutoUserAdmin):
    exclude = ('user', )
    inlines = [AddressInline, ]
    search_fields = ('name', 'email')
    raw_id_fields = ('country', )
    list_display = ('__str__', 'email')
    list_filter = (ClientCountryFilter, )


@admin.register(models.LoginEmail)
class LoginEmailAdmin(AutoUserAdmin):
    exclude = ('user', )
    list_display = ('login_id', 'email')
