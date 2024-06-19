from django.db import models

from account_module.models import User
from product_module.models import Product


# Create your models here.


class Order(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid= models.BooleanField(verbose_name='نهایی شده/نشده')
    payment_date= models.DateTimeField(null=True,blank=True,verbose_name='تاریخ پرداخت')

    def calculate_total_price(self):
        total_amount= 0
        if self.is_paid:
            for order_detail in self.orderdetails_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetails_set.all():
                total_amount += order_detail.product.price * order_detail.count
        return total_amount



    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name= 'سبد خرید محصول'
        verbose_name_plural= 'سبد های خرید محصول'

class OrderDetails(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    order= models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سبد خرید')
    final_price= models.IntegerField(null=True, blank=True,verbose_name='قیمت نهایی تکی محصول')
    count= models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.order
    class Meta:
        verbose_name= 'جزییات سبد خرید'
        verbose_name_plural= 'جزییات سبد های خرید'
