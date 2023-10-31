from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField()
    phone_number = models.CharField(max_length=11,unique=True)
    full_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    created = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number}-{self.code}'
