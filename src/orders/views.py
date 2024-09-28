from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
from orders.models import *
from django.contrib import messages


class CartView(TemplateView):
    template_name = 'order/shop-cart.html'


@method_decorator(login_required, name='dispatch')
class CheckOutView(TemplateView):
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(customer=self.request.user)
        addresses = Address.objects.filter(user=self.request.user)
        cart_products = CartProduct.objects.filter(cart=cart)

        for item in cart_products:
            item.total_price = item.product.price * item.quantity

        context['cart_products'] = cart_products
        context['cart_total'] = sum(item.total_price for item in cart_products)
        context['addresses'] = addresses  # Pass addresses to the template
        return context

    def post(self, request, *args, **kwargs):
        address_id = request.POST.get('address')
        if address_id:
            address = Address.objects.get(id=address_id)
            cart = Cart.objects.get(customer=self.request.user)
            cart_products = CartProduct.objects.filter(cart=cart)
            total_price = sum(item.product.price * item.quantity for item in cart_products)

            order = Order.objects.create(
                total_price=total_price,
                customer=request.user,
                address=address
            )

            for item in cart_products:
                OrderProduct.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_products.delete()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('orders:success')
        else:
            messages.error(request, 'Please select an address.')
            return redirect('orders:check_out')


class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'order/order_success.html'
