from django.db import models
from django.contrib.auth.models import User

#개인 학습용 주석 : 외부 키 이용하기 위해선 ForeignKey.
# 예를 들어, 정책평가 Author은 자신이 선택한다기 보단, 로그인 된 자신 정보를 가져오는 느낌임.
# on_delete=models.CASCAD은 솔직히 확신이 들지는 않음. 참조된 객체가 사라지면 (그니까 작성자가 사라지면? ) 그러면 자동으로 삭제되는 느낌인 것 같음.

# 글쓰기 기능을 위한 모델
class PolicyIdea(models.Model):
    title = models.CharField(max_length=200)  # 제목
    content = models.TextField()              # 내용
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
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

#사진 여러개 처리.
class PolicyImage(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="images") 
    image = models.ImageField(upload_to='policy_ideas/')  # 다중 이미지 처리용 필드


# 정책 아이디어 평가 모델 (1~5점 평가)
class Evaluation(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="evaluations")  # PolicyIdea와 연결
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 평가한 유저
    score = models.IntegerField()  # 예: 1~5점 평가

    def __str__(self):
        return f"Policy {self.policy.id} - User {self.user.id} - Score {self.score}"

    def save(self, *args, **kwargs):
        # 이미 평가한 기록이 있으면 삭제 후 새로운 평가로 수정
        existing_evaluation = Evaluation.objects.filter(policy=self.policy, user=self.user).first()
        if existing_evaluation:
            existing_evaluation.delete()  # 기존 평가 삭제
        super().save(*args, **kwargs)  # 새로운 평가 저장


# 좋아요 체크 모델
class Like(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="likes") #likes로 설정.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# 스크랩 기능 모델. 이거 나중에 USER을 기반으로 반환하면 마이 페이지에서 스크랩한 내용들 보여줄 수 있을 듯?
class Scrap(models.Model):
    policy = models.ForeignKey(PolicyIdea, on_delete=models.CASCADE, related_name="scraps") #scraps로 설정.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
