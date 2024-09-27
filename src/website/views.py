from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, ProductSearchForm
from django.db.models import Q


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class HomePageView(TemplateView):
    template_name = 'website/index.html'


class ProductListView(ListView):
    model = Product
    template_name = 'website/shop.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_active=True)
    paginate_by = 9


from django.views.generic.detail import DetailView
from .models import Product, Comment

from django.views.generic import DetailView
from .models import Product, Comment


class ProductDetailView(DetailView):
    model = Product
    template_name = 'website/product-details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object

        # Fetch approved comments, ordered by created_at (newest first)
        comments = Comment.objects.filter(product=product, approved=True).order_by('-created_at')
        context['comments'] = comments

        # Fetch related products, excluding the current product, ordered by id (or any preferred field)
        context['related_products'] = Product.objects.exclude(pk=product.pk).order_by('-id')[:4]

        return context


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'website/comment_form.html'

    def form_valid(self, form):
        # Fetch the product using the URL parameter
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        # Set the product and customer for the comment
        form.instance.product = product
        form.instance.customer = self.request.user  # Assuming `CustomUser` is used as `User`
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the product detail page or any other URL after successful comment creation
        return reverse_lazy('website:product_detail', kwargs={'pk': self.kwargs['pk']})


class ProductSearchView(ListView):
    model = Product
    template_name = 'website/product_search.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        query = self.request.GET.get('q', '')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(categories__title__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductSearchForm(self.request.GET or None)
        return context
