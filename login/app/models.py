from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email or not phone:
            raise ValueError("Users must have an email and phone")
        user = self.model(email=self.normalize_email(email), phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def generate_otp(self):
        self.otp = f"{random.randint(100000, 999999)}"
        self.save()
