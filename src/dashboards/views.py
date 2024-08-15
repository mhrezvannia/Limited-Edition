from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/customer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.request.user
        return context
