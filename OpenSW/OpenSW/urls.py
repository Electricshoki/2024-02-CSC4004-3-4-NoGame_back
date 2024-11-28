from django.contrib import admin
from django.urls import path, include
from PolicyUser.views import KakaoLoginView, KakaoCallbackView, KakaoLogoutView, KakaoUnlinkView, ModifyProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', KakaoLoginView.as_view(), name='kakao-login'),
    path('accounts/kakao/login/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),
    path('modify/', ModifyProfileView.as_view(), name='modify_profile'),
    path('logout/', KakaoLogoutView.as_view(), name='kakao-logout'),
    path('unlink/', KakaoUnlinkView.as_view(), name='kakao-unlink'),
    path('policy/', include('PolicyIdea.urls')),
    path('policyapp/', include('PolicyApp.urls')), 
]
