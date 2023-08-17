from django import forms
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.http import request


# Create your models here.

class AppUserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)



class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'email'

    objects = AppUserManager()

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )

    is_staff = models. BooleanField(
        default=False,
    )


    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('company', 'Company'),
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        blank=True,
        null=True,
    )

UserModel = get_user_model()

class RegularUserModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_motivation = models.TextField(max_length=600)

    user_telephone = models.CharField(max_length=50)

class CompanyUserModel(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_info = models.TextField(max_length=600)
    company_site = models.CharField(max_length=200)
    company_addres = models.CharField(max_length=200)
    logo = models.FileField(upload_to='company_logo/')


