from rest_framework import serializers
from .models import PolicyIdea, PolicyImage, Evaluation, Like, Scrap, Tag  # Tag 모델 추가

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']  # 필요한 필드만 추가

class PolicyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyImage
        fields = ['image']

class PolicyIdeaSerializer(serializers.ModelSerializer):
    images = PolicyImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    policy = serializers.PrimaryKeyRelatedField(queryset=PolicyIdea.objects.all(), required=False)
    tags = TagSerializer(many=True, required=False)  # 태그 필드 추가

    average_score = serializers.FloatField(read_only=True)

    class Meta:
        model = PolicyIdea
        fields = ['id', 'title', 'content', 'created_at', 'images', 'uploaded_images', 'average_score', 'user', 'policy', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        policy_idea = PolicyIdea.objects.create(**validated_data)
        for tag_data in tags_data:
            policy_idea.tags.add(tag_data)
        return policy_idea

class EvaluationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Evaluation
        fields = ['policy', 'score', 'user']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['policy', 'user']

class ScrapSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Scrap
        fields = ['policy', 'user']
