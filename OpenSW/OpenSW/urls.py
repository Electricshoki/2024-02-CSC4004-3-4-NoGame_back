from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('policy/', include('PolicyIdea.urls')),  # PolicyIdea의 URL 포함
]
