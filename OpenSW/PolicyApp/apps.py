from django.apps import AppConfig


class PolicyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PolicyApp'

    def ready(self):
        from crawlers.policy_crawler import fetch_and_save_policies
        fetch_and_save_policies()  # 서버 시작 시 크롤러 실행
