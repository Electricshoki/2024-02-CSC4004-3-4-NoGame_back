from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .models import User
from .serializers import UserSerializer

class KakaoLoginView(APIView):
    def get(self, request):
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        
        kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(kakao_auth_url)

class KakaoCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        client_secret = settings.KAKAO_CONFIG['KAKAO_CLIENT_SECRET']

        # 토큰 받기
        token_request = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )
        token_json = token_request.json()
        access_token = token_json.get("access_token")

        # 카카오 사용자 정보 받기
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")

        # 사용자 생성 또는 업데이트
        try:
            user = User.objects.get(kakao_id=profile_json.get("id"))
        except User.DoesNotExist:
            user = User.objects.create(
                username=f"kakao_{profile_json.get('id')}",
                kakao_id=profile_json.get("id"),
                nickname=profile.get("nickname"),
                profile_image=profile.get("profile_image_url"),
            )
        
        serializer = UserSerializer(user)
        return Response(serializer.data)