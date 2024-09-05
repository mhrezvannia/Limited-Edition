from django.urls import path
from .views import *

urlpatterns = [
    path('customer/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('vendor/', VendorDashboardView.as_view(), name='vendor_dashboard'),
    path('customer/<int:pk>/edit/', CustomerEditView.as_view(), name='customer_edit'),
    path('customer/<int:pk>/addresses/', CustomerAddressesView.as_view(), name='customer_addresses'),
    path('customer/<int:pk>/addresses/create/', CustomerAddressCreateView.as_view(), name='customer_create_address'),
    path('vendor/<int:pk>/', DashboardVendorDetailView.as_view(), name='dashboard_vendor_detail'),
    # path('employees/', VendorEmployeeListView.as_view(), name='employee-list'),
    # path('employees/<int:pk>/', VendorEmployeeDetailView.as_view(), name='employee-detail'),
    # path('employees/create/', VendorEmployeeCreateView.as_view(), name='employee-create'),
    # path('employees/<int:pk>/update/', VendorEmployeeUpdateView.as_view(), name='employee-update'),
    # path('employees/<int:pk>/delete/', VendorEmployeeDeleteView.as_view(), name='employee-delete'),

]
