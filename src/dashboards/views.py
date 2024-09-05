from django.views.generic import TemplateView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .forms import CustomerEditForm
from django.urls import reverse_lazy, reverse
from accounts.forms import AddressForm


from accounts.models import Customer, Address
from vendors.models import *
from website.models import *


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/customer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer,id=self.request.user.id)
        return context


class VendorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/vendor_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor'] = get_object_or_404(Vendor, owner_id=self.request.user.id)
        return context


class CustomerEditView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerEditForm
    success_url = reverse_lazy('customer_dashboard')
    template_name = 'dashboards/customer_edit.html'


class CustomerAddressesView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'dashboards/customer_addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer,id=self.request.user.id)
        return context


class CustomerAddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'dashboards/customer_create_address.html'

    def form_valid(self, form):
        try:
            customer = Customer.objects.get(pk=self.request.user.pk)
            form.instance.user = customer
        except Customer.DoesNotExist:
            return redirect('error_page')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('customer_addresses', kwargs={'pk': self.request.user.pk})

