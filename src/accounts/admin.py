from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Customer, Address
from .forms import CustomerSignUpForm, VendorOwnerSignUpForm


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    add_form = CustomerSignUpForm  # Use this for user creation in the admin interface

    list_display = ('email', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        # ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ('user_permissions', 'groups')


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('user__email', 'first_name', 'last_name')


class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ('user', 'zip_code', 'city', 'detail')
    search_fields = ('user__email', 'zip_code', 'city')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
