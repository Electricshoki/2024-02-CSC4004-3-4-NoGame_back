from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import PolicyIdeaViewSet, EvaluationViewSet, LikeViewSet, ScrapViewSet, TagViewSet, policyidea_detail

# 라우터 생성 및 뷰셋 등록
router = DefaultRouter()
router.register(r'policy_ideas', PolicyIdeaViewSet)  # 글쓰기 기능
router.register(r'evaluations', EvaluationViewSet)   # 평가 기능
router.register(r'likes', LikeViewSet)               # 좋아요 기능
router.register(r'scraps', ScrapViewSet)             # 스크랩 기능
router.register(r'tags', TagViewSet, basename='tag')  # 태그 등록

# URL 패턴 설정
urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/', policyidea_detail, name='policyidea_detail')
]

# MEDIA_URL을 처리하기 위한 설정 추가
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
