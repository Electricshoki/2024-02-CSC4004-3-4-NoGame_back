from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    kakao_id = models.CharField(max_length=100, unique=True, null=True) # 카카오톡 내부 ID
    nickname = models.CharField(max_length=100, blank=True) # 카카오톡 프로필 이름
    profile_image = models.URLField(blank=True) # 카카오톡 프로필 사진

    age = models.PositiveIntegerField(default=0)  # 나이
    gender = models.CharField(max_length=200)  # 성별
    residence = models.CharField(max_length=200)  # 거주지

    joined_at = models.DateTimeField(default=timezone.now)  # 가입시간 필드 (로그아웃, 탈퇴 기능 구현여부 확인용)
    access_token = models.TextField(null=True, blank=True)  # 토큰 필드 추가

    def __str__(self):
        return self.nickname