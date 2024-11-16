from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True) # 카카오톡 내부 ID
    nickname = models.CharField(max_length=100, blank=True) # 카카오톡 프로필 이름
    profile_image = models.URLField(blank=True) # 카카오톡 프로필 사진

    age = models.PositiveIntegerField(null=True, blank=True, default=0)  # 나이
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, default='')  # 성별
    email = models.EmailField(blank=True, default="")  # 이메일
    residence = models.CharField(max_length=255, blank=True, default="")  # 거주지