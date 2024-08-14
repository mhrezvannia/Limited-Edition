from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from vendors.models import Vendor, VendorEmployee
from accounts.models import Address, Customer, CustomUser
from vendors.models import VendorEmployee


# class LoginForms(forms.Form):
#
#     email = forms.EmailField()
#     password = forms.CharField(max_length=128)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['zip_code', 'city', 'detail']


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Customer
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
        return user


class VendorOwnerSignUpForm(UserCreationForm):
    vendor_name = forms.CharField(max_length=255)
    zip_code = forms.CharField(max_length=255, required=False)
    detail = forms.CharField(widget=forms.Textarea, required=True)
    city = forms.CharField(max_length=255, required=True)

    class Meta:
        model = VendorEmployee
        fields = ['email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'owner'  # Set the role to 'owner'
        if commit:
            user.save()
            # Create and save the Address instance
            address = Address.objects.create(
                zip_code=self.cleaned_data['zip_code'],
                detail=self.cleaned_data['detail'],
                city=self.cleaned_data['city'],
                user=user
            )
            # Create and save the Vendor instance
            vendor = Vendor.objects.create(
                name=self.cleaned_data['vendor_name'],
                address=address
            )
            # Assign the vendor to the user
            user.vendor = vendor
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Phone')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = CustomUser.objects.filter(email=username).first() or \
                       CustomUser.objects.filter(phone_number=username).first()

                if user and user.check_password(password):
                    self.user_cache = user
                else:
                    raise forms.ValidationError("اطلاعات وارد شده نامعتبر است")
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("اطلاعات وارد شده نامعتبر است")

        return self.cleaned_data
