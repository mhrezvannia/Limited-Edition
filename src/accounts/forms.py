from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from vendors.models import Vendor
from accounts.models import Address, VendorEmployee

# class LoginForms(forms.Form):
#
#     email = forms.EmailField()
#     password = forms.CharField(max_length=128)

CustomUser = get_user_model()


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['zip_code', 'city', 'detail']



