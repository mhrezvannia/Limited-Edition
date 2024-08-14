from django.contrib import admin
from .models import Vendor, VendorEmployee


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address')
    search_fields = ('name',)


@admin.register(VendorEmployee)
class VendorEmployeeAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'vendor', 'role')
    list_filter = ('role', 'vendor')
    search_fields = ('email', 'phone_number', 'vendor__name')