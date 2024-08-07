from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'has_discount',
                    'discount_type', 'discount_value',
                    'vendor', 'is_active')
    list_filter = ('vendor',)


@admin.register(ProductPicture)
class ProductPicture(admin.ModelAdmin):
    list_display = ('file_name', 'product')


@admin.register(Rate)
class Rate(admin.ModelAdmin):
    list_display = ('product', 'customer', 'star_count')


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('product', 'customer', 'approved')


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('__all__',)


@admin.register(ProductCategory)
class ProductCategory(admin.ModelAdmin):
    list_display = ('__all__',)
