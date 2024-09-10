from django.contrib import admin

from . import models


# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', ]


admin.site.register(models.User, AccountAdmin)
