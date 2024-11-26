from transformers import pipeline

# KoBERT 또는 KcBERT 모델 로드
sentiment_pipeline = pipeline("sentiment-analysis", model="beomi/kcbert-base")

def analyze_sentiment(text):
    """
    리뷰 텍스트의 감정을 분석하여 점수와 레이블 반환.
    """
    result = sentiment_pipeline(text)[0]  # 결과는 리스트의 첫 번째 항목
    return {
        "score": result["score"],  # 감정 점수 (0~1)
        "label": result["label"]   # 긍정(POSITIVE) 또는 부정(NEGATIVE)
    }
