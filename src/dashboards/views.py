from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from accounts.forms import CustomerSignUpForm

from accounts.models import Customer
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
    template_name = 'dashboards/customer_edit.html'
    model = Customer
    form_class = CustomerSignUpForm
    fields = ['name', 'last_name',]
