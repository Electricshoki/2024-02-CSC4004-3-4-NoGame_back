from django.shortcuts import redirect
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import User
import requests
from rest_framework import status

<<<<<<< HEAD
from django.http import JsonResponse
from rest_framework.decorators import api_view

=======
>>>>>>> upstream/main
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

        if not user.username:
            user.username = user.nickname

        user.save()

        request.session['user_id'] = user.id
        request.session['nickname'] = user.nickname
        request.session['profile_image'] = user.profile_image

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
        
class UserProfileView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "User not logged in."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user_info = {
            'username': user.username,
            'age': request.session.get('age', user.age if user.age else "Unknown"),
            'gender': request.session.get('gender', user.gender if user.gender else "Unknown"),
            'residence': request.session.get('residence', user.residence if user.residence else "Unknown"),
        }

        return Response({"user_info": user_info})

    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "User not logged in."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get("username", user.username)
        age = request.data.get("age", user.age if user.age else "Unknown")
        gender = request.data.get("gender", user.gender if user.gender else "Unknown")
        residence = request.data.get("residence", user.residence if user.residence else "Unknown")

        user.username = username
        user.age = age
        user.gender = gender
        user.residence = residence
        user.save()

        request.session['age'] = age
        request.session['gender'] = gender
        request.session['residence'] = residence

<<<<<<< HEAD
        return self.get(request)

@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "profile_image": user.profile_image,
            "age": user.age,
            "gender": user.gender,
            "residence": user.residence,
            "joined_at": user.joined_at.strftime('%Y-%m-%d %H:%M:%S'),
        }, json_dumps_params={'ensure_ascii': False}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
        
@api_view(['GET'])
def all_users(request):
    """
    모든 사용자 정보를 반환하는 함수
    """
    users = User.objects.all()
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "profile_image": user.profile_image,
            "age": user.age,
            "gender": user.gender,
            "residence": user.residence,
            "joined_at": user.joined_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for user in users
    ]
    return JsonResponse(user_list, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)    
=======
        return self.get(request)
>>>>>>> upstream/main
