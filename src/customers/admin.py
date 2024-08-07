from django.contrib import admin
from customers.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'zip_code')
    search_fields = ('city', 'user')
    list_filter = ('city',)
