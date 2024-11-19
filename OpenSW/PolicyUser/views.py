<<<<<<< HEAD
=======
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
#위 내용은 수정한 내용.
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .models import User
from .serializers import UserSerializer

<<<<<<< HEAD
=======
User = get_user_model()

>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
class KakaoLoginView(APIView):
    def get(self, request):
        # 카카오 로그인 URL 생성
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        
        # 카카오 로그인 인증 URL로 리다이렉트
        kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(kakao_auth_url)

class KakaoCallbackView(APIView):
    def get(self, request):
        # 카카오에서 제공한 인증 코드 받기
        code = request.GET.get("code")
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = settings.KAKAO_CONFIG['KAKAO_REDIRECT_URI']
        client_secret = settings.KAKAO_CONFIG['KAKAO_CLIENT_SECRET']

        # 인증 코드로 토큰 요청
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

        # 카카오 사용자 정보 요청
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")

        # 가입 유저가 있는지 확인하고, 없으면 ID 새로 생성
        user, created = User.objects.get_or_create(kakao_id=profile_json.get("id"))
        
        # 사용자 정보를 직렬화하여 반환
        serializer = UserSerializer(user)
<<<<<<< HEAD
        return Response(serializer.data)
=======
        return Response(serializer.data)
    

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
