from django.contrib import admin
from clients.models import Client, Country


class CountryAdmin(admin.ModelAdmin):
    # fields = ['cn_name', 'en_name', 'code', 'voltage', 'socket']
    list_display = ('cn_name', 'en_name', 'code', 'voltage', 'socket')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country')

admin.site.register(Client, ClientAdmin)
admin.site.register(Country, CountryAdmin)
