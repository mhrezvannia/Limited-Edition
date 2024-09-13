from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from dashboards.forms import CustomerEditForm, ProductCreateForm
from django.urls import reverse_lazy, reverse
from accounts.forms import AddressForm

from accounts.models import Customer, Address
from vendors.models import *
from website.models import *
from vendors.models import *
from vendors.forms import *


class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/customer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, id=self.request.user.id)
        return context


class VendorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/../templates/vendor/vendor_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor'] = get_object_or_404(Vendor, owner_id=self.request.user.id)
        context['employee'] = get_object_or_404(VendorEmployee, customuser_ptr=self.request.user)
        return context


class CustomerEditView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerEditForm
    success_url = reverse_lazy('customer_dashboard')
    template_name = 'customer/customer_edit.html'


class CustomerAddressesView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'dashboards/../templates/customer/customer_addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = get_object_or_404(Customer, id=self.request.user.id)
        return context


class CustomerAddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'dashboards/../templates/customer/customer_create_address.html'

    def form_valid(self, form):
        try:
            customer = Customer.objects.get(pk=self.request.user.pk)
            form.instance.user = customer
        except Customer.DoesNotExist:
            return redirect('error_page')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('customer_addresses', kwargs={'pk': self.request.user.pk})


class DashboardVendorDetailView(LoginRequiredMixin, DetailView):
    model = Vendor
    template_name = 'dashboards/../templates/vendor/vendor_detail.html'
    context_object_name = 'vendor'


class VendorEmployeeListView(LoginRequiredMixin, ListView):
    model = VendorEmployee
    template_name = 'dashboards/../templates/customer/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        vendor_id = self.kwargs.get('pk')
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        return VendorEmployee.objects.filter(vendor=vendor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor_pk'] = self.kwargs.get('pk')  # Add this line
        return context


class VendorEmployeeCreateView(CreateView):
    model = VendorEmployee
    form_class = VendorEmployeeForm
    template_name = 'dashboards/../templates/vendor/vendor_employee_create.html'
    success_url = reverse_lazy('vendor_employee_list', kwargs={'pk': '<vendor_pk>'})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['role'].choices = [(role, role_name) for role, role_name in form.fields['role'].choices if
                                       role != 'owner']
        return form


class VendorEmployeeUpdateView(UpdateView):
    model = VendorEmployee
    form_class = VendorEmployeeForm
    template_name = 'dashboards/../templates/vendor/vendor_employee_update.html'
    success_url = reverse_lazy('vendor_employee_list', kwargs={'pk': '<vendor_pk>'})

    def get_queryset(self):
        return VendorEmployee.objects.exclude(role='Owner')


class VendorEmployeeDeleteView(DeleteView):
    model = VendorEmployee
    template_name = 'vendor_employee_delete.html'
    success_url = reverse_lazy('vendor_employee_list')


class DashboardVendorEmployeeDetailView(LoginRequiredMixin, DetailView):
    model = VendorEmployee
    template_name = 'dashboards/../templates/vendor/vendor_employee_detail.html'
    context_object_name = 'employee'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'content', 'price', 'has_discount', 'discount_type',
              'discount_value', 'main_image']  # 'vendor' removed
    template_name = 'dashboards/../templates/vendor/product_create.html'
    success_url = reverse_lazy('vendor_dashboard')

    def form_valid(self, form):
        user = self.request.user

        # Get the VendorEmployee instance associated with the logged-in user
        vendor_employee = get_object_or_404(VendorEmployee, customuser_ptr=self.request.user)

        # Set the vendor on the product form instance
        form.instance.vendor = vendor_employee.vendor
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'dashboards/../templates/vendor/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        vendor_employee = get_object_or_404(VendorEmployee, customuser_ptr=self.request.user)
        vendor_id = vendor_employee.vendor.id
        return Product.objects.filter(vendor_id=vendor_id, is_active=True)
