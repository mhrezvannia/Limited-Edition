from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
import requests
from rest_framework import viewsets
from accounts.models import Address
from orders.models import Cart, CartProduct
from accounts.forms import AddressForm


class CartView(TemplateView):
    template_name = 'order/shop-cart.html'


class CheckOutView(TemplateView):
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            cart = Cart.objects.get(customer=self.request.user)
            customer = cart.customer
            addresses = Address.objects.filter(user=customer)
            cart_products = CartProduct.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart_products = []
            addresses = []

        for item in cart_products:
            item.total_price = item.product.price * item.quantity

        context['cart_products'] = cart_products
        context['cart_total'] = sum(item.total_price for item in cart_products)
        context['addresses'] = addresses
        context['address_form'] = AddressForm()
        return context

    def post(self, request, *args, **kwargs):
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.customer = request.user
            new_address.save()

            return self.get(request, *args, **kwargs)
        else:
            context = self.get_context_data(**kwargs)
            context['address_form'] = address_form
            return self.render_to_response(context)