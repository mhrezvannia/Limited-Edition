from django.urls import path
from .views import HomePageView


app_name = 'website'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('products', HomePageView.as_view(), name='products'),
]