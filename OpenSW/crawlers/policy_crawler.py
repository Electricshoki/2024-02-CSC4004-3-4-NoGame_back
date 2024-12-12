from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
<<<<<<< HEAD
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
=======

def fetch_policies_with_regions(max_pages=5): #기본 5페이지
    service = Service(r"C:\Users\dbgkw\Downloads\chromedriver-win64(130.0.6723.31)\chromedriver-win64\chromedriver.exe")# 요 친구 사용하는 사람에 따라서 위치 바뀌고 해야할 듯...
    driver = webdriver.Chrome(service=service)

    base_url = "https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?frameYn=Y&pageIndex="
    page_index = 1  # 첫 페이지
    policies = []

    while page_index <= max_pages:  # 최대 페이지 설정
        print(f"페이지 {page_index} 크롤링 중...")
        driver.get(base_url + str(page_index))
        time.sleep(3)  # 페이지 로딩 대기
>>>>>>> upstream/main

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

<<<<<<< HEAD
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
=======
        items = soup.select('.result-card-box')  # 정책 항목 값이던데.
        if not items:
            print("더 이상 데이터가 없습니다.")
            break  # 종료 조건.

        for item in items:
            try: # 값이 없을 수도 있으니 try로 진행.
                title_elem = item.select_one('.tit')
                proposal_date_elem = item.select_one('.dday')
                content_elem = item.select_one('.cover p')
                region_elem = item.select_one('.organ-name p')  # 지역 정보 요소

                # 값 추출 (NoneType일 경우 기본값 처리)
                title = title_elem.text.strip() if title_elem else "제목 없음"
                proposal_date = proposal_date_elem.text.strip() if proposal_date_elem else "날짜 없음"
                content = content_elem.text.strip() if content_elem else "내용 없음"
                region = region_elem.text.strip() if region_elem else "지역 정보 없음"

                # D-day 처리
                duration = int(proposal_date.replace('D-day ', '').replace('일', '')) if 'D-day' in proposal_date else 0

                # 정책 데이터 추가
                policies.append({
                    "title": title,
                    "proposal_date": proposal_date,
                    "duration": duration,
                    "content": content,
                    "region": region  # 지역 정보 추가
                })
            except Exception as e:
                print(f"데이터 추출 중 에러 발생: {e}")

        # 다음 페이지로 이동
        page_index += 1

    driver.quit()  # 드라이버 종료
    return policies

if __name__ == "__main__":
    max_pages = 10  #최대 페이지
    policies = fetch_policies_with_regions(max_pages=max_pages)
    for policy in policies:
        print(policy)
>>>>>>> upstream/main
