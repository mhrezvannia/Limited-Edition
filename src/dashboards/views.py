from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Customer
from vendors.models import *
from website.models import *


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/customer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(id=self.request.user.id)
        return context


class VendorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'vendoremployee'):
            vendor = user.vendoremployee.vendor
            context['vendor'] = vendor

        return context
