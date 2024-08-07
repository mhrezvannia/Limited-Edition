from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    phone = models.CharField(max_length=50, unique=True)

    # ROLES
    CUSTOMER = 0
    OWNER = 1
    MANAGER = 2
    OPERATOR = 3

    ROLE_CHOICES = (
        (OWNER, "Owner"),
        (CUSTOMER, 'Customer'),
        (MANAGER, 'Manager'),
        (OPERATOR, 'Operator')
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email
