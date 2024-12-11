from django.contrib import admin
from django.urls import path, include
from PolicyUser.views import KakaoLoginView, KakaoCallbackView, KakaoLogoutView, KakaoUnlinkView, UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', KakaoLoginView.as_view(), name='kakao-login'),
    path('accounts/kakao/login/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),
    path('user/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', KakaoLogoutView.as_view(), name='kakao-logout'),
    path('unlink/', KakaoUnlinkView.as_view(), name='kakao-unlink'),
    path('policyidea/', include('PolicyIdea.urls')),
    path('policyapp/', include('PolicyApp.urls')), 
    path('policyuser/', include('PolicyUser.urls')),
    
]
