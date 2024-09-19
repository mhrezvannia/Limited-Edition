from django.db import models
from accounts.models import CustomUser, Address
from vendors.models import Vendor
from django.core.validators import MinValueValidator, MaxValueValidator
from easy_thumbnails.fields import ThumbnailerImageField


class Category(models.Model):
    title = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='category_pics/', null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        (0, 'Percentage'),
        (1, 'Fixed Amount'),
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Consider decimal_places=2 for monetary values
    has_discount = models.BooleanField(default=False)
    discount_type = models.IntegerField(choices=DISCOUNT_TYPE_CHOICES, default=0, blank=True, null=True)
    discount_value = models.FloatField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    main_image = ThumbnailerImageField(upload_to='product/main_images', null=True, blank=True)
    in_stock = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, blank=True)
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
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.customer.email} - {self.product.title}'


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'category')
        verbose_name_plural = 'product categories'
