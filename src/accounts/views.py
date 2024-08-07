from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('') # TODO add url here

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(CustomLoginView, self).form_valid(form)


def logoutview(request):
    logout(request)
    return redirect('') # TODO add url here