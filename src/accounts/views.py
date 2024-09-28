from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, DetailView
from accounts.forms import *
from .forms import *
from django.contrib.auth import authenticate, login


# class CustomLoginView(View):
#     template_name = 'login.html'
#
#     def get(self, request):
#         form = CustomLoginForm()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = CustomLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('website:index')
#             else:
#                 form.add_error(None, 'Invalid email or password.')
#         return render(request, self.template_name, {'form': form})


# def logoutview(request):
#     logout(request)
#     return redirect('website:index')

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('website:index')


class CustomerSignUpView(CreateView):
    model = Customer
    form_class = CustomerSignUpForm
    template_name = 'accounts/register_customer.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(FormView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('website:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class VendorLoginView(FormView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboards:vendor_dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class OwnerSignUpView(CreateView):
    form_class = VendorOwnerSignUpForm
    template_name = 'accounts/vendor_register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return redirect('accounts:login')
