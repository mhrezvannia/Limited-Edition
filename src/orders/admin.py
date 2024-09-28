from django.contrib import admin
from .models import DiscountCode, Order, OrderProduct, Cart, CartProduct


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = (
     'code', 'customer', 'discount_type', 'discount_value',
     'expiration_date', 'usage_count', 'remain_count',
     'is_activate')
    search_fields = ('code', 'customer__email')
    list_filter = ('discount_type', 'is_activate', 'expiration_date')
    ordering = ('expiration_date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'created_at', 'updated_at', 'discount_code', 'address')
    search_fields = ('customer__email',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'status')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__created_at', 'status')
    ordering = ('order__created_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')
    search_fields = ('customer__email',)
    ordering = ('id',)


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__id', 'product__name')
    list_filter = ('cart__id',)
    ordering = ('cart__id',)
