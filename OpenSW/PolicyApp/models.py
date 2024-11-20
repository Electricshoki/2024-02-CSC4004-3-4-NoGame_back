from django.db import models

# Create your models here.
class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False) #제목      
    content = models.CharField(max_length=6000,null=False,default=0) #글내용
    created_at = models.DateTimeField(auto_now_add=True) #게시글 생성일 자동 생성
    ing = models.BooleanField(default=0, null=False)  #마감/진행중여부표시
    #images = models.ManyToManyField('PolicyImage', related_name='policies')
    
    
class PolicyImage(models.Model):
    policy = models.ForeignKey(Policy, related_name='images', on_delete=models.CASCADE)  # 다중 이미지와 연결
    image = models.ImageField(upload_to='policy_images/')  # 이미지 파일 저장 경로