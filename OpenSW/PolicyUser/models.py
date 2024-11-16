from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=100, blank=True)
    profile_image = models.URLField(blank=True)
    kakao_id = models.CharField(max_length=100, unique=True, null=True)