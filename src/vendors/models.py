from django.db import models

from django.db import models
from accounts.models import CustomUser, Address


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='owned_vendors', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


