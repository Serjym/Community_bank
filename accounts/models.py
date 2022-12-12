from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    mailing_address = models.CharField(max_length=200, blank=True)
    college = models.CharField(max_length=30)
    major = models.CharField(max_length=30)
    