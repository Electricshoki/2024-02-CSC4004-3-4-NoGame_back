from django.shortcuts import redirect
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import User
import requests
from rest_framework import status

User = get_user_model()

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

        token_request = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )
        token_json = token_request.json()
        access_token = token_json.get("access_token")

        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")

        user, created = User.objects.get_or_create(kakao_id=profile_json.get("id"))
        user.nickname = profile.get("nickname")
        user.profile_image = profile.get("profile_image_url")
        user.access_token = access_token
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class KakaoLogoutView(APIView):
    def get(self, request):
        client_id = settings.KAKAO_CONFIG['KAKAO_REST_API_KEY']
        logout_redirect_uri = settings.KAKAO_CONFIG['LOGOUT_REDIRECT_URI']
        kakao_logout_url = f"https://kauth.kakao.com/oauth/logout?client_id={client_id}&logout_redirect_uri={logout_redirect_uri}"
        return redirect(kakao_logout_url)   

class KakaoUnlinkView(APIView):
    def get(self, request):
        return Response(
            {"message": "This endpoint only supports POST requests for unlinking."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def post(self, request):
        # 로그인된 사용자의 액세스 토큰 가져오기
        user = request.user
        access_token = getattr(user, "access_token", None)

        if not access_token:
            return Response({"error": "Access token not found for user."}, status=status.HTTP_400_BAD_REQUEST)

        # 카카오 API 연결 끊기 요청
        unlink_url = "https://kapi.kakao.com/v1/user/unlink"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        response = requests.post(unlink_url, headers=headers)

        if response.status_code == 200:
            # 연결 끊기 성공
            user.delete()  # 연결 끊기 성공 시 사용자 삭제
            return Response({"message": "Account successfully unlinked and user deleted."}, status=status.HTTP_200_OK)
        else:
            # 실패한 경우
            return Response(
                {"error": "Failed to unlink account.", "response": response.json()},
                status=status.HTTP_400_BAD_REQUEST,
            )