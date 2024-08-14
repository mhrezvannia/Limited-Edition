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


class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password1', 'password2']


class VendorOwnerSignUpForm(UserCreationForm):
    vendor_name = forms.CharField(max_length=255)
    vendor_address = AddressForm()

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            address = self.cleaned_data['vendor_address']
            address.save()
            vendor = Vendor.objects.create(
                name=self.cleaned_data.get('vendor_name'),
                address=address,
                owner=user
            )
        return user


class VendorEmployeeForm(forms.ModelForm):
    class Meta:
        model = VendorEmployee
        fields = ['user', 'role']


