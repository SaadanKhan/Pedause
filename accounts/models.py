from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15)
    otp = models.IntegerField(null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True) 
    is_verified = models.BooleanField(default=False)
    govt_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return str(self.phone)


class SocialAccount(models.Model):

    ACCOUNT_TYPES = [
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('apple', 'Apple')
    ]

    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank= True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15)
    apple_id = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, choices=ACCOUNT_TYPES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name