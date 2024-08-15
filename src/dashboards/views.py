from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from vendors.models import *
from website.models import *


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/customer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.request.user
        return context


class VendorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Dashboards-templates/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'vendoremployee'):
            vendor = user.vendoremployee.vendor
            context['vendor'] = vendor  # Add vendor information

        return context
