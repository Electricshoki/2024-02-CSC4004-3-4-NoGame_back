from django.db import models
from django.conf import settings
from PolicyApp.models import Policy

class PolicyIdea(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='policy_ideas/', blank=True, null=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="ideas", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="policy_ideas", null=True, blank=True)

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
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='policy_ideas/')

class Evaluation(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="evaluations")
    score = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )

    def __str__(self):
        return f"Policy {self.policy.id} - Score {self.score}"

class Like(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )

class Scrap(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="scraps")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scraps"
    )
