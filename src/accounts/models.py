from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email field is required')
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=50)
    phone = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

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
    REQUIRED_FIELDS = []

    Objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
