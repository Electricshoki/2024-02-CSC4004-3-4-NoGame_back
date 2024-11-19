from rest_framework import viewsets
from .models import PolicyIdea, Evaluation, Like, Scrap
from .serializers import PolicyIdeaSerializer, EvaluationSerializer, LikeSerializer, ScrapSerializer
from rest_framework.permissions import IsAuthenticated

class PolicyIdeaViewSet(viewsets.ModelViewSet):
    queryset = PolicyIdea.objects.all()
    serializer_class = PolicyIdeaSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ScrapViewSet(viewsets.ModelViewSet):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
