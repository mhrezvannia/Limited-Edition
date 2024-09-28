from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
import requests
from rest_framework import viewsets

from orders.models import Cart

class CartView(TemplateView):
    template_name = 'order/shop-cart.html'


