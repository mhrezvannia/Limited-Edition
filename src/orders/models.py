from django.db import models
from accounts.models import User
from customers.models import Address
from website.models import Product


class DiscountCode(models.Model):
    code = models.CharField(max_length=255)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_type = models.IntegerField(default=0)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiration_date = models.DateTimeField(blank=True, null=True)
    usage_count = models.IntegerField(default=0)
    remain_count = models.IntegerField(blank=True, null=True)
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order {self.id} by {self.customer.email}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
