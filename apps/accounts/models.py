from django.core.management.base import BaseCommand
from datetime import timedelta
# from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import *
from django.utils import timezone
from django.core.files.storage import default_storage
from apps.tools.compressor import *
# from django_ckeditor_5.fields import CKEditor5Field
from django.db.models import Max
from datetime import datetime

# Create your models here.

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others'),
]
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30, blank=True, default='User')
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=None, blank=True, null=True)

    photo = models.ImageField(upload_to='userPhotos', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_ec_member = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        try:
            old_instance = User.objects.get(pk=self.pk)
            if self.photo != old_instance.photo:
                if old_instance.photo:
                    default_storage.delete(old_instance.photo.path)
                # Compress the new image
                self.photo = compress_image(self.photo, 50)
        except:  # Create mode
            if self.photo:
                self.photo = compress_image(self.photo, 50)
        super().save(*args, **kwargs)


class TemporaryOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def is_valid(self):
        return self.created_at + timedelta(minutes=1) > timezone.now()

    def delete_if_expired(self):
        """Deletes the OTP if it's expired."""
        if self.created_at + timedelta(minutes=1) < timezone.now():
            self.delete()

    def __str__(self):
        remaining_time = (self.created_at + timedelta(minutes=1)) - timezone.now()
        return f"OTP for {self.User.email}, expires in {remaining_time.seconds} seconds."

    def save(self, *args, **kwargs):
        TemporaryOTP.objects.filter(
            created_at__lte=timezone.now() - timedelta(minutes=1)).delete()
        super().save(*args, **kwargs)
