from django.db import models
<<<<<<< HEAD
=======
from django.conf import settings  # AUTH_USER_MODEL 가져오기
from PolicyApp.models import Policy  # Policy 모델 가져오기
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)

# 글쓰기 기능을 위한 모델
class PolicyIdea(models.Model):
    title = models.CharField(max_length=200)  # 제목
    content = models.TextField()              # 내용
<<<<<<< HEAD
    created_at = models.DateTimeField(auto_now_add=True)        # 작성 시간
    image = models.ImageField(upload_to='policy_ideas/', blank=True, null=True)  # 이미지 필드 추가...
=======
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    image = models.ImageField(upload_to='policy_ideas/', blank=True, null=True)  # 이미지 필드 추가

    # Policy 모델과 연결
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="ideas", null=True, blank=True, default=1)


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="policy_ideas",
        null=True,
        blank=True
    )
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)

    def __str__(self):
        return self.title

<<<<<<< HEAD
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

=======
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
# 사진 여러 개 처리
class PolicyImage(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='policy_ideas/')  # 다중 이미지 처리용 필드

<<<<<<< HEAD
=======

>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
# 정책 아이디어 평가 모델 (1~5점 평가)
class Evaluation(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="evaluations")  # PolicyIdea와 연결
    score = models.IntegerField()  # 예: 1~5점 평가
<<<<<<< HEAD
=======
    user = models.ForeignKey(  # 평가를 남긴 사용자 정보
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)

    def __str__(self):
        return f"Policy {self.policy.id} - Score {self.score}"

<<<<<<< HEAD
# 좋아요 체크 모델
class Like(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="likes")
=======

# 좋아요 체크 모델
class Like(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(  # 좋아요를 남긴 사용자 정보
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )

>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)

# 스크랩 기능 모델
class Scrap(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="scraps")
<<<<<<< HEAD
=======
    user = models.ForeignKey(  # 스크랩한 사용자 정보
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scraps"
    )
>>>>>>> 23c6b36 (feat: Added user, policy model to policyidea model)
