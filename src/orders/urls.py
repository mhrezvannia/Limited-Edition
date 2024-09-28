from django.urls import path, include
from orders.views import *
app_name = 'orders'
urlpatterns = [
    path('api/v1/', include('orders.api.v1.urls')),
    path('cart/',CartView.as_view(), name='cart'),
]