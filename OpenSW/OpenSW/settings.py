from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 미디어 파일 경로 설정.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = 'django-insecure-=za$5@xyys(-8z+s4-q-)yg@+7++up#pqmq1xzebqi3os+*r=p'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
  
    'rest_framework', # rest api 사용
    'rest_framework.authtoken',
  
    'PolicyIdea',
    'PolicyApp',
    'PolicyUser',
]

<<<<<<< HEAD
#-----------------------실제 인증 할 때------------------------------
#REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': [
#        'rest_framework.authentication.SessionAuthentication',  # 세션
#        'rest_framework.authentication.TokenAuthentication',    # 토큰
#    ],
#    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.IsAuthenticated',           # 인증된 사용자만 접근 허용
#    ],
#}

#---------------테스트 할 때 ---------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # 인증 비활성화
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # 인증 없이 접근 허용
    ],
}


=======
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# rest api 관련 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY": "48fbbd944370c44ffd825a0a7ca01074",      # kakao REST API key
    "KAKAO_REDIRECT_URI": "http://127.0.0.1:8000/accounts/kakao/login/callback/", # kakao redirect url
    "KAKAO_CLIENT_SECRET": "tmfu0j7GwflUaPAzHcRQ6m9DZ69Ib41e"     # kakao client secret key
}

ROOT_URLCONF = 'OpenSW.urls'

AUTH_USER_MODEL = 'PolicyUser.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'OpenSW.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Static 파일 저장소
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
