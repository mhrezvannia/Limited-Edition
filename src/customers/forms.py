from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth import authenticate

from accounts.models import User


class CustomerCreationForm(forms.ModelForm):

    password2 = forms.CharField(label='Password_confirm', widget=forms.PasswordInput, max_length=20)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("passwords doesn't match")
        return password2
