from rest_framework import serializers
<<<<<<< HEAD
from .models import PolicyIdea, PolicyImage, Evaluation, Like, Scrap
=======
from PolicyApp.models import Policy
from .models import PolicyIdea, PolicyImage, Evaluation, Like, Scrap
from django.contrib.auth import get_user_model

User = get_user_model()
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)

class PolicyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyImage
        fields = ['image']

<<<<<<< HEAD
# serializers.py
=======
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
class PolicyIdeaSerializer(serializers.ModelSerializer):
    images = PolicyImageSerializer(many=True, read_only=True)  # 다중 이미지
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
<<<<<<< HEAD
    )  # 필드를 선택적으로 만듦

    # 평균 평점 추가
    average_score = serializers.FloatField(read_only=True)

    class Meta:
        model = PolicyIdea
        fields = ['id', 'title', 'content', 'created_at', 'images', 'uploaded_images', 'average_score']
=======
    )  # 업로드 이미지를 위한 필드
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )  # 선택 가능하도록 설정
    policy = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.all(), required=True
    )  # 선택 가능하도록 설정

    average_score = serializers.FloatField(read_only=True)  # 평균 평점

    class Meta:
        model = PolicyIdea
        fields = [
            'id', 'title', 'content', 'created_at', 'images', 'uploaded_images',
            'average_score', 'user', 'policy'  # user와 policy 필드 추가
        ]
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        policy_idea = PolicyIdea.objects.create(**validated_data)
<<<<<<< HEAD
        # 이미지가 제공되었으면 저장
        for image in uploaded_images:
            PolicyImage.objects.create(policy=policy_idea, image=image)
        return policy_idea

# 평가 기능을 위한 시리얼라이저
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['policy', 'score']  # 'user' 필드 제거
    
# 좋아요 기능을 위한 시리얼라이저
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['policy']  # 'user' 필드 제거

# 스크랩 기능을 위한 시리얼라이저
class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap
        fields = ['policy']  # 'user' 필드 제거
=======
        for image in uploaded_images:
            PolicyImage.objects.create(policy=policy_idea, image=image)
        return policy_idea
class EvaluationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # 사용자 필드

    class Meta:
        model = Evaluation
        fields = ['policy', 'score', 'user']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # 사용자 필드

    class Meta:
        model = Like
        fields = ['policy', 'user']

class ScrapSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # 사용자 필드

    class Meta:
        model = Scrap
        fields = ['policy', 'user']
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
