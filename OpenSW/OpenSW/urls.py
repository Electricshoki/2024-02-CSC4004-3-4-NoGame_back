from django.contrib import admin
from django.urls import path, include
from rest_auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 로그인
    path('account/', include('rest_auth.urls')),
    path('account/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    url(r'account/registration/confirm-email/(?P<key>.+)/$', confirm_email, name='confirm_email'),
    path('', include('django.contrib.auth.urls')),
]
