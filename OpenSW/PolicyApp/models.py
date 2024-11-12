from django.db import models

# Create your models here.
class Policy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100) #제목
    content = models.CharField #글내용
    created_at = models.DateTimeField(auto_now_add=True) #게시글 생성일 자동 생성
    status = models.BooleanField  #마감/진행중여부표시
    #image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)