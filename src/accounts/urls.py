from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', CustomerSignUpView.as_view(), name='register'),
    path('vendor_register/', OwnerSignUpView.as_view(), name='vendor_register'),
    path('vendor_login/', VendorLoginView.as_view(), name='vendor_login'),
]
