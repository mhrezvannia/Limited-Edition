from django.urls import path
from .views import CartCreateAPIView, AddItemAPIView, RemoveItemAPIView, UpdateItemAPIView, ViewCartAPIView

urlpatterns = [
    path('cart/create/', CartCreateAPIView.as_view(), name='cart_create'),
    path('cart/add/', AddItemAPIView.as_view(), name='add_item'),
    path('cart/remove/', RemoveItemAPIView.as_view(), name='remove_item'),
    path('cart/update/', UpdateItemAPIView.as_view(), name='update_item'),
    path('cart/view/', ViewCartAPIView.as_view(), name='view_cart'),
]
