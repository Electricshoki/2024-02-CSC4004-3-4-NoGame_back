from django.db import models

# 글쓰기 기능을 위한 모델
class PolicyIdea(models.Model):
    title = models.CharField(max_length=200)  # 제목
    content = models.TextField()              # 내용
    created_at = models.DateTimeField(auto_now_add=True)        # 작성 시간
    image = models.ImageField(upload_to='policy_ideas/', blank=True, null=True)  # 이미지 필드 추가...

    def __str__(self):
        return self.title

    # 평균 평점 계산
    @property
    def average_score(self):
        evaluations = self.evaluations.all()  # 관련된 평가 가져오기
        if evaluations.count() > 0:
            total_score = sum(evaluation.score for evaluation in evaluations)
            return total_score / evaluations.count()  # 평균 계산
        return 0  # 평가가 없으면 0 반환

    # 좋아요 수 계산
    def like_count(self):
        return self.likes.count()  # 'likes'는 PolicyIdea 모델과 연결된 Like 객체들

# 사진 여러 개 처리
class PolicyImage(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='policy_ideas/')  # 다중 이미지 처리용 필드

# 정책 아이디어 평가 모델 (1~5점 평가)
class Evaluation(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="evaluations")  # PolicyIdea와 연결
    score = models.IntegerField()  # 예: 1~5점 평가

    def __str__(self):
        return f"Policy {self.policy.id} - Score {self.score}"

# 좋아요 체크 모델
class Like(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="likes")

# 스크랩 기능 모델
class Scrap(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="scraps")
