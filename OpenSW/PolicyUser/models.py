from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True) # 카카오톡 내부 ID
    nickname = models.CharField(max_length=100, blank=True) # 카카오톡 프로필 이름
    profile_image = models.URLField(blank=True) # 카카오톡 프로필 사진

    age = models.PositiveIntegerField()  # 나이
    gender = models.CharField(max_length=200)  # 성별
    residence = models.CharField(max_length=200)  # 거주지