from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import CustomerSignUpForm


class CustomerRegisterView(View):
    def get(self, request):
        form = CustomerSignUpForm()
        context = {'form': form}
        return render(request, 'register_customer.html', context)

    def post(self, request):
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.role = 0
            customer.set_password(form.cleaned_data['password'])
            customer.save()
            return redirect('website:index')
        return render(request, 'register_customer.html', {'form': form})
