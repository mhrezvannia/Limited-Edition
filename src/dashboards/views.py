from django.http import HttpResponseNotFound
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from dashboards.forms import CustomerEditForm, ProductCreateForm, VendorEditForm
from django.urls import reverse_lazy, reverse
from accounts.forms import AddressForm

from accounts.models import Customer, Address
from orders.models import Order, OrderProduct
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
    template_name = 'vendor/vendor_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor'] = get_object_or_404(Vendor, owner_id=self.request.user.id)
        context['employee'] = get_object_or_404(VendorEmployee, customuser_ptr=self.request.user)
        return context


class VendorEditView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorEditForm
    success_url = reverse_lazy('dashboards:vendor_dashboard')
    template_name = 'vendor/vendor_update.html'

    def get_object(self):
        vendor_employee = get_object_or_404(VendorEmployee, id=self.request.user.id)
        vendor = get_object_or_404(Vendor, id=vendor_employee.vendor_id)
        return vendor


class CustomerEditView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerEditForm
    success_url = reverse_lazy('dashboards:customer_dashboard')
    template_name = 'customer/customer_edit.html'

    def get_object(self):
        return self.request.user.customer


class CustomerAddressesView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'customer/customer_addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.request.user.customer
        return context


class CustomerAddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'customer/customer_create_address.html'

    def form_valid(self, form):
        try:
            customer = self.request.user.customer
            form.instance.user = customer
        except Customer.DoesNotExist:
            return redirect('error_page')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboards:customer_addresses')


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'customer/customer_confirm_delete.html'

    def get_object(self):
        address_id = self.request.POST.get('address_id')
        return Address.objects.get(pk=address_id, user=self.request.user)

    def get_success_url(self):
        return reverse('dashboards:customer_addresses')


class AddressEditView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'customer/customer_edit_address.html'

    def get_object(self, queryset=None):
        address_id = self.request.GET.get('address_id')
        if address_id:
            return get_object_or_404(Address, pk=address_id, user=self.request.user)
        return redirect('error_page')

    def get_success_url(self):
        return reverse('dashboards:customer_addresses')


class DashboardVendorDetailView(LoginRequiredMixin, DetailView):
    model = Vendor
    template_name = 'vendor/vendor_detail.html'
    context_object_name = 'vendor'

    def get_object(self):
        if hasattr(self.request.user, 'vendoremployee'):
            vendor_employee = self.request.user.vendoremployee
            return get_object_or_404(Vendor, pk=vendor_employee.vendor.pk)
        return get_object_or_404(Vendor, owner=self.request.user)


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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'vendor/product_create.html'
    success_url = reverse_lazy('dashboards:product_list')

    def form_valid(self, form):
        user = self.request.user
        vendor_employee = get_object_or_404(VendorEmployee, customuser_ptr=user)
        form.instance.vendor = vendor_employee.vendor
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        user = self.request.user
        vendor_employee = get_object_or_404(VendorEmployee, customuser_ptr=user)
        context = super().get_context_data(**kwargs)
        context['vendor'] = vendor_employee.vendor
        return context


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'vendor/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        vendor_employee = get_object_or_404(VendorEmployee, customuser_ptr=user)
        vendor = vendor_employee.vendor
        return Product.objects.filter(vendor=vendor, is_active=True)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'vendor/product_confirm_delete.html'
    success_url = reverse_lazy('dashboards:product_list')


class ProductEditView(UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'vendor/product_edit.html'
    success_url = reverse_lazy('dashboards:product_list')


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'customer/comment_list.html'
    context_object_name = 'Comments'
    paginate_by = 12

    def get_queryset(self):
        return Comment.objects.filter(customer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(customer=self.request.user)
        context['comments'] = comments
        return context


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'customer/customer_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.request.user.customer
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'customer/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Correctly fetch the order products related to this order
        context['order_products'] = OrderProduct.objects.filter(order=self.object)
        return context
