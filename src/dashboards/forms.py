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
        fields = [
            'title', 'content', 'price', 'has_discount', 'discount_type', 'discount_value'
            , 'main_image', 'in_stock', 'categories', 'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Product Title'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Description'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Price'})
        self.fields['has_discount'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['discount_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Discount Type'})
        self.fields['discount_value'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Discount Value'})
        self.fields['main_image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['in_stock'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Stock Quantity'})
        self.fields['categories'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})


class VendorEmployeeFm(forms.ModelForm):
    class Meta:
        model = VendorEmployee
        fields = ('vendor', 'role', 'email', 'phone_number')


class VendorEditForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address']


