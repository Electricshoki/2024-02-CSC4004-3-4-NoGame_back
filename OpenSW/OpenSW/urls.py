from django.contrib import admin
from django.urls import path, include
from PolicyUser.views import KakaoLoginView, KakaoCallbackView

urlpatterns = [
    path('admin/', admin.site.urls),
  
    path('', KakaoLoginView.as_view(), name='kakao-login'),
    path('accounts/kakao/login/callback/', KakaoCallbackView.as_view(), name='kakao-callback'),
  
    path('admin/', admin.site.urls),
    path('policy/', include('PolicyIdea.urls')),  # PolicyIdea의 URL 포함
]
