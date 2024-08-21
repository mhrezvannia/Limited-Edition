from django.db import models
from accounts.models import CustomUser , Address
from vendors.models import Vendor
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    has_discount = models.BooleanField(default=False)
    discount_type = models.IntegerField(default=0)
    discount_value = models.FloatField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='product/main_images', null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProductPicture(models.Model):
    title = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='product_pics/', null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Rate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    star_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.customer.email} - {self.product.title}'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.customer.email} - {self.product.title}'


class Category(models.Model):
    title = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='category_pics/', null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'category')
        verbose_name_plural = 'product categories'
