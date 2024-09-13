from django.urls import path
from .views import *

app_name = 'dashboards'
urlpatterns = [
    path('customer/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('vendor/', VendorDashboardView.as_view(), name='vendor_dashboard'),
    path('customer/<int:pk>/edit/', CustomerEditView.as_view(), name='customer_edit'),
    path('customer/<int:pk>/addresses/', CustomerAddressesView.as_view(), name='customer_addresses'),
    path('customer/<int:pk>/addresses/create/', CustomerAddressCreateView.as_view(), name='customer_create_address'),
    path('vendor/<int:pk>/', DashboardVendorDetailView.as_view(), name='dashboard_vendor_detail'),
    path('vendor/product/create/', ProductCreateView.as_view(), name='product_create'),
    path('vendor/product/', ProductListView.as_view(), name='product_list'),
    path('vendor/<int:pk>/employees/', VendorEmployeeListView.as_view(), name='vendor_employee_list'),
    path('vendor/employees/<int:pk>/', DashboardVendorEmployeeDetailView.as_view(), name='employee-detail'),
    path('vendor/employee/create/', VendorEmployeeCreateView.as_view(), name='vendor_employee_create'),
    path('dashboards/vendor/<pk>/employees/<employee_pk>/update/', VendorEmployeeUpdateView.as_view(),
         name='vendor_employee_update'),
    # path('vendor-employee/<int:pk>/delete/', VendorEmployeeDeleteView.as_view(), name='vendor_employee_delete'),

]
