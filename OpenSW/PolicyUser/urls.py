from django.urls import path
from .views import user_detail, all_users

urlpatterns = [
    path('user/<int:user_id>/', user_detail, name='user-detail'),  # 특정 사용자 정보 조회
    path('users/', all_users, name='all-users'),  # 모든 사용자 정보 조회
]
