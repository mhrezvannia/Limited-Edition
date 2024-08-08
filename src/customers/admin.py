from django.contrib import admin
from customers.models import Address, City


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'zip_code')
    search_fields = ('city', 'user')
    list_filter = ('city',)


@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ('name',)

