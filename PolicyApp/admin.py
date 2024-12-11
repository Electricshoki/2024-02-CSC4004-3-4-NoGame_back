from django.contrib import admin
from .models import *
# Register your models here.

class PolicyImageInline(admin.TabularInline):  # Inline 설정
    model = PolicyImage
    extra = 1  # 빈 이미지 입력 필드 추가 개수

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0  # 기존 별점만 표시 (추가 입력 필드 없음)

class PolicyAdmin(admin.ModelAdmin):  # Policy에 이미지 인라인 추가
    inlines = [PolicyImageInline]
    

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'policy', 'score', 'review', 'created_at']  # 표시할 필드
    list_filter = ['score', 'created_at']  # 필터 설정
    search_fields = ['user__username', 'policy__title', 'review']  # 검색 필드


admin.site.register(Policy, PolicyAdmin)  # Policy 모델 등록
admin.site.register(Rating, RatingAdmin)