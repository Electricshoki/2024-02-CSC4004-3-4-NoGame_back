from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PolicyIdea, Evaluation, Like, Scrap, Tag
from .serializers import ( PolicyIdeaSerializer, EvaluationSerializer, LikeSerializer, ScrapSerializer, TagSerializer)


from django.db.models import Avg
from django.http import JsonResponse

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        tag_name = request.data.get('name', None)
        if not tag_name:
            return Response({'detail': '태그 이름은 필수입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)
        return Response({'detail': '이미 존재하는 태그입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_tag(self, request, pk=None):
        tag = self.get_object()
        tag.delete()
        return Response({'detail': '태그가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('name', None)
        if query:
            tags = Tag.objects.filter(name__icontains=query)
            return Response(TagSerializer(tags, many=True).data, status=status.HTTP_200_OK)
        return Response({'detail': '검색어를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)


class PolicyIdeaViewSet(viewsets.ModelViewSet):
    queryset = PolicyIdea.objects.all()
    serializer_class = PolicyIdeaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return PolicyIdea.objects.filter(user=self.request.user)

    @action(detail=True, methods=['delete'])
    def delete_policy(self, request, pk=None):
        policy = self.get_object()
        if policy.user != request.user:
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        policy.delete()
        return Response({'detail': '정책 아이디어가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put', 'patch'])
    def update_policy(self, request, pk=None):
        policy = self.get_object()
        if policy.user != request.user:
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(policy, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], url_path='delete_evaluation/(?P<policy_id>[^/.]+)')
    def delete_evaluation(self, request, policy_id=None):
        evaluation = get_object_or_404(Evaluation, policy_id=policy_id, user=request.user)
        evaluation.delete()
        return Response({'detail': '평가가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], url_path='delete_like/(?P<policy_id>[^/.]+)')
    def delete_like(self, request, policy_id=None):
        like = get_object_or_404(Like, policy_id=policy_id, user=request.user)
        like.delete()
        return Response({'detail': '좋아요가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


class ScrapViewSet(viewsets.ModelViewSet):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], url_path='delete_scrap/(?P<policy_id>[^/.]+)')
    def delete_scrap(self, request, policy_id=None):
        scrap = get_object_or_404(Scrap, policy_id=policy_id, user=request.user)
        scrap.delete()
        return Response({'detail': '스크랩이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


def policyidea_detail(request, id):
    try:
        # 요청받은 ID에 해당하는 정책 아이디어 조회
        policy_idea = PolicyIdea.objects.get(pk=id)

        # 연결된 태그 조회
        tags = [tag.name for tag in policy_idea.tags.all()]

        # 좋아요 및 스크랩 수
        like_count = Like.objects.filter(policy=policy_idea).count()
        scrap_count = Scrap.objects.filter(policy=policy_idea).count()

        # 평가 데이터
        evaluations = Evaluation.objects.filter(policy=policy_idea)
        average_score = evaluations.aggregate(Avg('score'))['score__avg']
        total_evaluations = evaluations.count()

        # 이미지 URL 목록
        images = policy_idea.policyidea_images.all()
        image_urls = [image.image.url for image in images]

        return JsonResponse({
            'id': policy_idea.id,
            'title': policy_idea.title,
            'content': policy_idea.content,
            'created_at': policy_idea.created_at,
            'tags': tags,
            'like_count': like_count,
            'scrap_count': scrap_count,
            'average_score': average_score,
            'total_evaluations': total_evaluations,
            'images': image_urls,
        }, json_dumps_params={'ensure_ascii': False})
    except PolicyIdea.DoesNotExist:
        return JsonResponse({'error': 'PolicyIdea not found'}, status=404)