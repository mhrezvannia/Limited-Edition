from django import forms
from .models import Vendor, VendorEmployee


class VendorEmployeeForm(forms.ModelForm):
    class Meta:
        model = VendorEmployee
        fields = ['vendor', 'role']