from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomerCreationForm


class CustomerRegisterView(View):
    def get(self, request):
        form = CustomerCreationForm()
        context = {'form': form}
        return render(request, 'register_customer.html', context)

    def post(self, request):
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.role = 0
            customer.save()
            # return redirect
        return render(request, 'register_customer.html', {'form': form})
