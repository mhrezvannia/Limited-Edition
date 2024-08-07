from django.db import models
from accounts.models import User


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(models.Model):
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    detail = models.TextField()
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.detail}, {self.city.name}'
