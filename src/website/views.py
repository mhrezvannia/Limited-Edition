from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *


class ContactView(TemplateView):
    template_name = 'contact.html'


class HomePageView(TemplateView):
    template_name = 'index.html'


class ProductListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_active=True)
    paginate_by = 9


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-details.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['title', 'content', 'price', 'has_discount', 'discount_type', 'discount_value', 'vendor', 'is_active']


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['title', 'content', 'price', 'has_discount', 'discount_type', 'discount_value', 'vendor', 'is_active']


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'categories/category_form.html'
    fields = ['title', 'parent_category', 'image']


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'categories/category_form.html'
    fields = ['title', 'parent_category', 'image']


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


class RateCreateView(CreateView):
    model = Rate
    template_name = 'rates/rate_form.html'
    fields = ['product', 'customer', 'star_count']


class RateUpdateView(UpdateView):
    model = Rate
    template_name = 'rates/rate_form.html'
    fields = ['product', 'customer', 'star_count']


class RateDeleteView(DeleteView):
    model = Rate
    template_name = 'rates/rate_confirm_delete.html'
    success_url = reverse_lazy('product_list')
