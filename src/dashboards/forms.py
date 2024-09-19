from django import forms
from accounts.models import Customer
from website.models import Product
from vendors.models import VendorEmployee, Vendor


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'has_discount', 'discount_type',
                  'discount_value', 'vendor', 'main_image']


class VendorEmployeeForm(forms.ModelForm):
    class Meta:
        model = VendorEmployee
        fields = ('vendor', 'role', 'email', 'phone_number')


class VendorEditForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address']
