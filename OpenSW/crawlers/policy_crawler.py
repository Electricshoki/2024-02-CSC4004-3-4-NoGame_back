from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from PolicyApp.models import Policy  # Django 모델 불러오기

def fetch_and_save_policies(max_pages=5):  # 데이터 저장 포함
    service = Service(r"C:\Users\dbgkw\Downloads\chromedriver-win64(130.0.6723.31)\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    base_url = "https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?frameYn=Y&pageIndex="
    page_index = 1
    policies = []

    while page_index <= max_pages:
        print(f"페이지 {page_index} 크롤링 중...")
        driver.get(base_url + str(page_index))
        time.sleep(3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.select('.result-card-box')
        if not items:
            print("더 이상 데이터가 없습니다.")
            break

        for item in items:
            try:
                title_elem = item.select_one('.tit')
                content_elem = item.select_one('.cover p')
                title = title_elem.text.strip() if title_elem else "제목 없음"
                content = content_elem.text.strip() if content_elem else "내용 없음"

                # 데이터를 Policy 모델에 저장
                Policy.objects.update_or_create(
                    title=title,
                    defaults={"content": content, "ing": True}  # 진행 중으로 설정
                )
            except Exception as e:
                print(f"데이터 저장 중 에러 발생: {e}")

        page_index += 1

    driver.quit()
    print("크롤링 및 저장 완료")