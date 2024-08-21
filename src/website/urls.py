from django.urls import path
from .views import *


app_name = 'website'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('Contact/', ContactView.as_view(), name='contact'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/new/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    path('rates/new/', RateCreateView.as_view(), name='rate_create'),
    path('rates/<int:pk>/edit/', RateUpdateView.as_view(), name='rate_update'),
    path('rates/<int:pk>/delete/', RateDeleteView.as_view(), name='rate_delete'),

]