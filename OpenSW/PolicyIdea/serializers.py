from rest_framework import serializers
from .models import PolicyIdea, PolicyImage, Evaluation, Like, Scrap

class PolicyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyImage
        fields = ['image']

# serializers.py
class PolicyIdeaSerializer(serializers.ModelSerializer):
    images = PolicyImageSerializer(many=True, read_only=True)  # 다중 이미지
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )  # 필드를 선택적으로 만듦

    # 평균 평점 추가
    average_score = serializers.FloatField(read_only=True)

    class Meta:
        model = PolicyIdea
        fields = ['id', 'title', 'content', 'author', 'created_at', 'images', 'uploaded_images', 'average_score']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        policy_idea = PolicyIdea.objects.create(**validated_data)
        # 이미지가 제공되었으면 저장
        for image in uploaded_images:
            PolicyImage.objects.create(policy=policy_idea, image=image)
        return policy_idea

# 평가 기능을 위한 시리얼라이저
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['policy', 'user', 'score']
    
# 좋아요 기능을 위한 시리얼라이저
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['policy', 'user']

# 스크랩 기능을 위한 시리얼라이저
class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap
        fields = ['policy', 'user']
