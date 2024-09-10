from django.db import models

from account_module.models import User
from product_module.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='نهایی شده/نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت',)

    def get_order_total_price(self):
        total_price = 0

        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_price += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_price += order_detail.product.price * order_detail.count
        return total_price



    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی محصول')
    count = models.IntegerField(verbose_name='تعداد محصول')

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'لیست جزئیات سبد های خرید'