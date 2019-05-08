from django.contrib import admin

from .models import *


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


def update_build_price(modeladmin, request, queryset):
    for i in queryset:
        i.update_price()


class BuildAdmin(admin.ModelAdmin):
    readonly_fields = ('price',)

    actions = [update_build_price]

    list_display = (
        '__str__',
        'price',
        'cpu',
        'ram',
        'gpu',
    )


class UserBuildAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'User Build'
        verbose_name_plural = 'User Builds'


admin.site.register(Pc, PcAdmin)
admin.site.register(Monitor)
admin.site.register(Tag)
admin.site.register(UserBuild)
admin.site.register(Helper)
admin.site.register(Peripheral)

admin.site.register(Build, BuildAdmin)
