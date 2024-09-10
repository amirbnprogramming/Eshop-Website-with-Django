from django.contrib import admin
from . import models


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'subject',  'email', 'created_time', 'is_read_by_admin']
    list_filter = ['created_time', 'is_read_by_admin']


admin.site.register(models.ContactUs, ContactAdmin)
