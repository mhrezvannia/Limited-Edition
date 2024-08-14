from django.db import models

from django.db import models
from accounts.models import CustomUser, Address


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='owned_vendors', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class VendorEmployee(CustomUser):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('product_manager', 'Product Manager'),
        ('operator', 'Operator'),
    )

    vendor = models.ForeignKey(Vendor, related_name='employees', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('phone_number', 'vendor', 'role')

    def __str__(self):
        return f"{self.email} {self.phone_number} - {self.role}"
