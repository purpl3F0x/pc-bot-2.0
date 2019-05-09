from django.contrib import admin

from .models import Admin, AllowedChannel, BlackUser

# Register your models here.


admin.site.register(Admin)
admin.site.register(BlackUser)
admin.site.register(AllowedChannel)
