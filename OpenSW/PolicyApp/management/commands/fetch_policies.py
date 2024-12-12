from django.core.management.base import BaseCommand
from PolicyApp.policy_crawler import fetch_and_save_policies

class Command(BaseCommand):
    help = 'Fetch policies from the youthcenter website and save them to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("크롤링을 시작합니다...")
        fetch_and_save_policies(max_pages=5)
        self.stdout.write("크롤링이 완료되었습니다!")
