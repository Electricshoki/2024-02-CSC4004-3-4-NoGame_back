from rest_framework import serializers
from .models import PolicyIdea, PolicyImage, Evaluation, Like, Scrap

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

    average_score = serializers.FloatField(read_only=True)

    class Meta:
        model = PolicyIdea
        fields = ['id', 'title', 'content', 'created_at', 'images', 'uploaded_images', 'average_score', 'user', 'policy']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        policy_idea = PolicyIdea.objects.create(**validated_data)
        for image in uploaded_images:
            PolicyImage.objects.create(policy=policy_idea, image=image)
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
