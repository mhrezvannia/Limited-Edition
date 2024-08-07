from django.db import models

from django.db import models
from accounts.models import User
from customers.models import Address


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class VendorUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)