from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError('email field is required')
#         user = self.model(email=email)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password):
#         user = self.create_user(email=email, password=password)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('The Email or Phone number must be set')

        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, phone_number=phone_number, **extra_fields)
        else:
            user = self.model(phone_number=phone_number, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, phone_number, password, **extra_fields)


# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True, max_length=50)
#     phone = models.CharField(max_length=50, unique=True)
#     first_name = models.CharField(max_length=255, null=True)
#     last_name = models.CharField(max_length=255, null=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     # ROLES
#     CUSTOMER = 0
#     OWNER = 1
#     MANAGER = 2
#     OPERATOR = 3
#
#     ROLE_CHOICES = (
#         (OWNER, "Owner"),
#         (CUSTOMER, 'Customer'),
#         (MANAGER, 'Manager'),
#         (OPERATOR, 'Operator')
#     )
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.email
#
#     @property
#     def is_staff(self):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return True
#
#     def has_perm(self, perm, obj=None):
#         return True


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.email if self.email else self.phone_number


class Customer(CustomUser):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email


class Address(models.Model):
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    detail = models.TextField()
    city = models.CharField(max_length=255)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.detail}, {self.city}'



