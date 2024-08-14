from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.contrib.auth import authenticate, login


class CustomLoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForms()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForms(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('website:index')
            else:
                form.add_error(None, 'Invalid email or password.')
        return render(request, self.template_name, {'form': form})


# def logoutview(request):
#     logout(request)
#     return redirect('website:index')

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('website:index')
