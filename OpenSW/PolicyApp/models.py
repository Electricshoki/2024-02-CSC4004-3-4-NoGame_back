from django.db import models
from django.conf import settings
from PolicyUser.models import User

# Create your models here.
class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False) #제목      
    content = models.CharField(max_length=6000,null=False,default=0) #글내용
    created_at = models.DateTimeField(auto_now_add=True) #게시글 생성일 자동 생성
    ing = models.BooleanField(default=0, null=False)  #마감/진행중여부표시
    
    
    
class PolicyImage(models.Model):
    policy = models.ForeignKey(Policy, related_name='images', on_delete=models.CASCADE)  # 다중 이미지와 연결
    image = models.ImageField(upload_to='policy_images/')  # 이미지 파일 저장 경로
    
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'policy')  # 사용자당 하나의 좋아요만 허용

class Scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scraps')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='scraps')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'policy')  # 사용자당 하나의 스크랩만 허용

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='ratings')
    score = models.DecimalField(max_digits=3, decimal_places=1)  # 10점 만점, 소수점 1자리
    review = models.TextField(blank=True)  # 한줄평
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'policy')  # 사용자당 하나의 별점만 허용