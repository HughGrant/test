from django.contrib import admin
from products.models import Basic, Keyword


class BasicAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'cost', 'size',
                    'volume_weight', 'voltage', 'video')

admin.site.register(Keyword)
admin.site.register(Basic, BasicAdmin)
