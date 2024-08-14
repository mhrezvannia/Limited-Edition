from django.db import models
from accounts.models import CustomUser


# class City(models.Model):
#     name = models.CharField(max_length=255)
#
#     class Meta:
#         verbose_name_plural = 'Cities'
#
#     def __str__(self):
#         return self.name


# class Address(models.Model):
#     zip_code = models.CharField(max_length=255, blank=True, null=True)
#     detail = models.TextField()
#     city = models.CharField(max_length=255)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.detail}, {self.city}'
