from django.contrib import admin

from order_module.models import Order, OrderDetail


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'payment_date']


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'final_price', 'count']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
