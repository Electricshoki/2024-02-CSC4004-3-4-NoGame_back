from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rating
from .utils import analyze_sentiment

@receiver(post_save, sender=Rating)
def calculate_sentiment(sender, instance, **kwargs):
    """
    Rating 모델이 저장될 때 감정 분석 수행.
    """
    if instance.review:  # 리뷰가 존재할 때만 분석
        sentiment = analyze_sentiment(instance.review)
        instance.sentiment_score = sentiment["score"]
        instance.sentiment_label = sentiment["label"]
        instance.save()
