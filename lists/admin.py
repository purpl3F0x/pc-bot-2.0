from django.contrib import admin
from .models import Pc,Tag,Monitor

# Register your models here.
class PcAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'price',
        'cpu',
        'ram',
        'gpu',
        'comment',
        'active',
    )
    filter_horizontal = ('tags',)


admin.site.register(Pc,PcAdmin)
admin.site.register(Monitor)
admin.site.register(Tag)
