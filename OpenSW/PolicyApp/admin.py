from django.contrib import admin
from .models import Policy, PolicyImage
# Register your models here.

class PolicyImageInline(admin.TabularInline):  # Inline 설정
    model = PolicyImage
    extra = 1  # 빈 이미지 입력 필드 추가 개수

class PolicyAdmin(admin.ModelAdmin):  # Policy에 이미지 인라인 추가
    inlines = [PolicyImageInline]

admin.site.register(Policy, PolicyAdmin)  # Policy 모델 등록