from django.contrib import admin
from django.urls import path
from PolicyUser.views import KakaoLoginView, KakaoCallbackView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', KakaoLoginView.as_view(), name='kakao-login'),
    path('accounts/kakao/login/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),
]
