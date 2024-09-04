from django.urls import path
from .views import *

urlpatterns = [
    path('customer/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('vendor/', VendorDashboardView.as_view(), name='vendor_dashboard')
]
