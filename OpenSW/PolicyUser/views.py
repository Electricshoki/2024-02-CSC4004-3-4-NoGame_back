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

        # 토큰 요청
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

        # 프로필 요청
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")

        # 사용자 정보 생성 또는 업데이트
        user, created = User.objects.get_or_create(kakao_id=profile_json.get("id"))
        user.nickname = profile.get("nickname")
        user.profile_image = profile.get("profile_image_url")
        user.access_token = access_token
        user.save()

        # 세션에 사용자 정보 저장
        request.session['user_id'] = user.id  # 세션에 사용자 ID 저장
        request.session['nickname'] = user.nickname
        request.session['profile_image'] = user.profile_image

        # 사용자 정보 반환
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
        user = request.user
        access_token = getattr(user, "access_token", None)

        if not access_token:
            return Response({"error": "Access token not found for user."}, status=status.HTTP_400_BAD_REQUEST)

        unlink_url = "https://kapi.kakao.com/v1/user/unlink"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        response = requests.post(unlink_url, headers=headers)

        if response.status_code == 200:
            user.delete()
            return Response({"message": "Account successfully unlinked and user deleted."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Failed to unlink account.", "response": response.json()},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

class ModifyProfileView(APIView):
    def get(self, request):
        # 세션에서 사용자 정보 가져오기
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "User not logged in."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user_info = {
            'nickname': request.session.get('nickname', user.nickname),
            'profile_image': request.session.get('profile_image', user.profile_image),
            'age': request.session.get('age', 'Unknown'),
            'gender': request.session.get('gender', 'Unknown'),
            'residence': request.session.get('residence', 'Unknown'),
        }

        return Response({"user_info": user_info})

    def post(self, request):
        # 세션에서 사용자 정보 가져오기
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "User not logged in."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        
        # 세션에서 받은 새로운 값들로 업데이트
        nickname = request.data.get("nickname", user.nickname)
        profile_image = request.data.get("profile_image", user.profile_image)
        age = request.data.get("age", "Unknown")
        gender = request.data.get("gender", "Unknown")
        residence = request.data.get("residence", "Unknown")

        user.nickname = nickname
        user.profile_image = profile_image
        user.age = age
        user.gender = gender
        user.residence = residence
        user.save()

        # 세션 정보 업데이트
        request.session['nickname'] = nickname
        request.session['profile_image'] = profile_image
        request.session['age'] = age
        request.session['gender'] = gender
        request.session['residence'] = residence

        return Response({"message": "Profile updated successfully."})