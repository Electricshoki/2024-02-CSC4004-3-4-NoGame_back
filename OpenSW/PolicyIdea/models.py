from django.db import models
from django.conf import settings
from PolicyApp.models import Policy

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PolicyIdea(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='policy_ideas/', blank=True, null=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="policy_ideas", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_policy_ideas",null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='policy_ideas', blank=True)  # 태그 필드 추가

    def __str__(self):
        return self.title

    # 평균 평점 계산
    @property
    def average_score(self):
        evaluations = self.evaluations.all()
        if evaluations.count() > 0:
            total_score = sum(evaluation.score for evaluation in evaluations)
            return total_score / evaluations.count()
        return 0

    # 좋아요 수 계산
    def like_count(self):
        return self.likes.count()


class PolicyImage(models.Model):
    policy = models.ForeignKey(
        PolicyIdea, 
        on_delete=models.CASCADE, 
        related_name="policyidea_images"  # 고유하게 변경
    )
    image = models.ImageField(upload_to='policy_ideas/')


class Evaluation(models.Model):
    policy = models.ForeignKey(
        PolicyIdea, 
        on_delete=models.CASCADE, 
        related_name="policyidea_evaluations"  # 고유하게 변경
    )
    score = models.IntegerField()
    review = models.CharField(max_length=1000, blank=True)  # 한 줄 평 추가 (최대 1000자)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_evaluations"  # 고유하게 변경
    )

    def __str__(self):
        return f"Policy {self.policy.id} - Score {self.score} - Review: {self.review}"


class Like(models.Model):
    policy = models.ForeignKey(
        PolicyIdea, 
        on_delete=models.CASCADE, 
        related_name="policyidea_likes"  # 고유하게 변경
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_idea_likes"  # 고유하게 변경
    )


class Scrap(models.Model):
    policy = models.ForeignKey(
        PolicyIdea, 
        on_delete=models.CASCADE, 
        related_name="policyidea_scraps"  # 고유하게 변경
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_idea_scraps"  # 고유하게 변경
    )
