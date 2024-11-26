from django.db import models 
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Policy, PolicyImage, Like, Scrap, Rating
from .serializers import PolicySerializer, PolicyImageSerializer, LikeSerializer, ScrapSerializer, RatingSerializer

from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET','POST'])
def policy_list_create(request):
    
    if request.method == 'GET':
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        policy_serializer = PolicySerializer(data=request.data)
        if policy_serializer.is_valid(raise_exception=True):
            policy = policy_serializer.save()  # Policy 객체 저장
            
            # 다중 이미지 처리
            images = request.FILES.getlist('images')
            for image in images:
                PolicyImage.objects.create(policy=policy, image=image)
            
            return Response(data=PolicySerializer(policy).data)



@api_view(['POST'])
def like_policy(request, policy_id):
    policy = Policy.objects.get(id=policy_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, policy=policy)
    if not created:
        like.delete()
        return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
    return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def scrap_policy(request, policy_id):
    policy = Policy.objects.get(id=policy_id)
    user = request.user
    scrap, created = Scrap.objects.get_or_create(user=user, policy=policy)
    if not created:
        scrap.delete()
        return Response({'message': 'Scrap removed'}, status=status.HTTP_200_OK)
    return Response({'message': 'Scrapped'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def rate_policy(request, policy_id):
    policy = Policy.objects.get(id=policy_id)
    user = request.user
    score = request.data.get('score')
    review = request.data.get('review', '')
    rating, created = Rating.objects.update_or_create(
        user=user,
        policy=policy,
        defaults={'score': score, 'review': review}
    )
    return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_ratings(request, policy_id):
    ratings = Rating.objects.filter(policy_id=policy_id)
    serializer = RatingSerializer(ratings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def policy_sentiment_analysis(request, policy_id):
    """
    정책에 대한 리뷰의 평균 감정 점수를 반환하는 API.
    """
    try:
        policy = Policy.objects.get(id=policy_id)
        ratings = Rating.objects.filter(policy=policy)

        if not ratings.exists():
            return Response({"message": "No reviews available for this policy."})

        # 평균 감정 점수 계산
        avg_score = ratings.aggregate(models.Avg('sentiment_score'))['sentiment_score__avg']
        positive_count = ratings.filter(sentiment_label="POSITIVE").count()
        negative_count = ratings.filter(sentiment_label="NEGATIVE").count()

        return Response({
            "policy_id": policy_id,
            "title": policy.title,
            "average_sentiment_score": avg_score,
            "positive_reviews": positive_count,
            "negative_reviews": negative_count,
            "total_reviews": ratings.count(),
        })
    except Policy.DoesNotExist:
        return Response({"error": "Policy not found."}, status=404)