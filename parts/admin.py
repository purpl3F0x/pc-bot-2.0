from django.contrib import admin

from .models import *


class PartAdmin(admin.ModelAdmin):
    readonly_fields = ('last_modified', 'price', 'name',)
    ordering = ('name',)

    list_display = ('__str__', 'price', 'last_modified',)


# Register your models here.

admin.site.register(CPU, PartAdmin)
admin.site.register(Motherboard, PartAdmin)
admin.site.register(RAM, PartAdmin)
admin.site.register(GPU, PartAdmin)
admin.site.register(PSU, PartAdmin)
admin.site.register(Case, PartAdmin)
admin.site.register(Cooler, PartAdmin)
admin.site.register(Part, PartAdmin)
