from django import forms


class LoginForms(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(max_length=128)

