import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=64, null=True, blank=True) 
    profile_picture = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=256, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    
