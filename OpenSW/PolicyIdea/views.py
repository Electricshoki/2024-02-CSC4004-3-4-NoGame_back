from rest_framework import viewsets
from .models import PolicyIdea, Evaluation, Like, Scrap
from .serializers import PolicyIdeaSerializer, EvaluationSerializer, LikeSerializer, ScrapSerializer
from rest_framework.permissions import IsAuthenticated

# 글쓰기 기능을 위한 뷰셋
class PolicyIdeaViewSet(viewsets.ModelViewSet):
    queryset = PolicyIdea.objects.all()
    serializer_class = PolicyIdeaSerializer
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

# 평가 기능을 위한 뷰셋
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

# 좋아요 기능을 위한 뷰셋
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

# 스크랩 기능을 위한 뷰셋
class ScrapViewSet(viewsets.ModelViewSet):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]
