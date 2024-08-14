from django.urls import path
from .views import CustomerSignUpView, CustomLogoutView, CustomLoginView, OwnerSignUpView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomerSignUpView.as_view(), name='register'),
    path('Vendor_register/', OwnerSignUpView.as_view, name='vendor_register'),
]
