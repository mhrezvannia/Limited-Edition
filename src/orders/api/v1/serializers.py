# orders/serializers.py

from rest_framework import serializers
from orders.models import Cart, CartProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'main_image']


# class CartProductSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)
#
#     class Meta:
#         model = CartProduct
#         fields = ['id', 'product', 'quantity', 'status']


class CartProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True)



class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(source='cartproduct_set', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'products']
