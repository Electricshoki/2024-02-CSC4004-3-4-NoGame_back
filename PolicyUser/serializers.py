from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'kakao_id', 'nickname', 'profile_image', 'username', 'age', 'gender', 'residence', 'joined_at', 'access_token')
