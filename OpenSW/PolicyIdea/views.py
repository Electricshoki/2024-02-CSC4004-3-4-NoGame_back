from rest_framework import viewsets
from .models import PolicyIdea, Evaluation, Like, Scrap
from .serializers import PolicyIdeaSerializer, EvaluationSerializer, LikeSerializer, ScrapSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# 글쓰기 기능을 위한 뷰셋
class PolicyIdeaViewSet(viewsets.ModelViewSet):
    queryset = PolicyIdea.objects.all()
    serializer_class = PolicyIdeaSerializer
    permission_classes = [AllowAny]  # 테스트 단계에서는 인증 안 거침

    def perform_create(self, serializer):
        # 요청에서 user 값을 받아서 처리
        if not serializer.validated_data.get('user'):
            serializer.save(user=self.request.user)  # 로그인된 사용자로 설정
        else:
            serializer.save()

# 평가 기능을 위한 뷰셋
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [AllowAny]  # 테스트 단계에서는 인증 안 거침

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 좋아요 기능을 위한 뷰셋
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]  # 테스트 단계에서는 인증 안 거침

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 스크랩 기능을 위한 뷰셋
class ScrapViewSet(viewsets.ModelViewSet):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer
    permission_classes = [AllowAny]  # 테스트 단계에서는 인증 안 거침

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
