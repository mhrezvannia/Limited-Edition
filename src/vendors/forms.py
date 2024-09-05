from django import forms
from .models import Vendor, VendorEmployee


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'is_active']


class VendorEmployeeForm(forms.ModelForm):
    class Meta:
        model = VendorEmployee
        fields = ['email', 'phone_number', 'vendor', 'role', 'is_active']
        widgets = {
            'role': forms.Select(choices=[('product_manager', 'Product Manager'), ('operator', 'Operator')])
        }
