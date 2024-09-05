from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Vendor, VendorEmployee
from .forms import VendorForm, VendorEmployeeForm



class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Ensure the user is an owner
        return self.request.user.role == 'owner'


# Mixin to ensure only vendors owned by the current user are accessible
class VendorOwnerAccessMixin(UserPassesTestMixin):
    def test_func(self):
        vendor = self.get_object()
        return vendor.owner == self.request.user


# Mixin to ensure employees are accessible only to their respective vendor's owner
class EmployeeVendorOwnerAccessMixin(UserPassesTestMixin):
    def test_func(self):
        employee = self.get_object()
        return employee.vendor.owner == self.request.user


# Vendor CRUD Views
class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'vendor/vendor_list.html'
    context_object_name = 'vendors'

    def get_queryset(self):
        # Show only vendors owned by the current user
        return Vendor.objects.filter(owner=self.request.user)


class VendorDetailView(LoginRequiredMixin, VendorOwnerAccessMixin, DetailView):
    model = Vendor
    template_name = 'vendor/vendor_detail.html'
    context_object_name = 'vendor'


class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/vendor_form.html'
    success_url = reverse_lazy('vendor-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner from the logged-in user
        return super().form_valid(form)


class VendorUpdateView(LoginRequiredMixin, VendorOwnerAccessMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/vendor_form.html'
    success_url = reverse_lazy('vendor-list')


class VendorDeleteView(LoginRequiredMixin, VendorOwnerAccessMixin, DeleteView):
    model = Vendor
    template_name = 'vendor/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendor-list')


# VendorEmployee CRUD Views
class VendorEmployeeListView(LoginRequiredMixin, ListView):
    model = VendorEmployee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return VendorEmployee.objects.filter(vendor_owner=self.request.user)


class VendorEmployeeDetailView(LoginRequiredMixin, EmployeeVendorOwnerAccessMixin, DetailView):
    model = VendorEmployee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'


class VendorEmployeeCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = VendorEmployee
    form_class = VendorEmployeeForm
    template_name = 'employee/employee_form.html'
    success_url = reverse_lazy('employee-list')

    def form_valid(self, form):
        # Set the vendor to the current user's vendor and ensure only 'product_manager' and 'operator' roles can be assigned
        form.instance.vendor = get_object_or_404(Vendor, owner=self.request.user)
        if form.instance.role not in ['product_manager', 'operator']:
            form.add_error('role', 'Only Product Manager and Operator roles are allowed.')
            return self.form_invalid(form)
        return super().form_valid(form)


class VendorEmployeeUpdateView(LoginRequiredMixin, EmployeeVendorOwnerAccessMixin, UpdateView):
    model = VendorEmployee
    form_class = VendorEmployeeForm
    template_name = 'employee/employee_form.html'
    success_url = reverse_lazy('employee-list')


class VendorEmployeeDeleteView(LoginRequiredMixin, EmployeeVendorOwnerAccessMixin, DeleteView):
    model = VendorEmployee
    template_name = 'employee/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')
