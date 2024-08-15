from django.urls import path
from .views import *

urlpatterns = [
    path('customer/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('employee/', VendorDashboardView.as_view(), name='employee_dashboard')
]
