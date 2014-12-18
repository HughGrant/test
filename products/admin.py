from django.contrib import admin
from products.models import Basic, Keyword
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
