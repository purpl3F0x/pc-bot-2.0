from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import *


# Register your models here.


def update_build_price(modeladmin, request, queryset):
    for i in queryset:
        i.update_price()


class BuildAdmin(MarkdownxModelAdmin):
    readonly_fields = ('price',)
    actions = [update_build_price]
    list_display = ('__str__', 'price', 'cpu', 'motherboard', 'ram', 'gpu', 'psu', 'cooler')
    ordering = ('price',)

    filter_horizontal = ('case', 'others')

    def save_related(self, request, form, formset, change):
        if not change:  # Adding a new object
            form.save()  # Must be done before M2M save
        form.save_m2m()
        form.save()


class UserBuildAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'User Build'
        verbose_name_plural = 'User Builds'


admin.site.register(Monitor)
admin.site.register(Helper)
admin.site.register(Peripheral)

admin.site.register(Build, BuildAdmin)
