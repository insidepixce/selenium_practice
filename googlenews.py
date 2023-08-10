import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from PIL import Image
from openpyxl import Workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 검색어 입력
search_query = input("검색어를 입력하세요: ")

# Selenium WebDriver 설정
driver = webdriver.Chrome()
driver.get("https://www.youtube.com/")

# 검색어 입력란에 검색어 입력
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys(search_query)

# Enter 키 입력
search_box.send_keys(Keys.RETURN)

# 스크롤 및 영상 정보 수집
video_data = []
scroll_pause_time = 2
scroll_limit = 5  # 스크롤 횟수 제한

for scroll in range(scroll_limit):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    # 영상 정보 스크래핑
    video_elements = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")

    for video_element in video_elements:
        # 영상 정보 스크래핑 (이전 코드와 동일)
        title = video_element.find_element(By.ID, "video-title").text
        sanitized_title = re.sub(r'[^\w\s]', '', title)

        # 썸네일 컨테이너 대기
        wait = WebDriverWait(driver, 10)
        thumbnail_container = wait.until(EC.presence_of_element_located((By.ID, "thumbnail")))

        # 썸네일 스크린샷 저장
        thumbnail_path = f"movies/{search_query}/{sanitized_title}.png"
        driver.execute_script("arguments[0].style.visibility='visible';", thumbnail_container)
        driver.save_screenshot(thumbnail_path)
        driver.execute_script("arguments[0].style.visibility='hidden';", thumbnail_container)

        video_data.append({
            "title": sanitized_title,
            "thumbnail_path": thumbnail_path
        })

# 스크래핑된 영상 정보를 엑셀에 저장
wb = Workbook()
ws = wb.active

for data in video_data:
    row = [
        data["thumbnail_path"],
        data["title"]
    ]
    ws.append(row)

excel_path = f"YOUTUBE/{search_query}/{search_query}_excel.xlsx"
wb.save(excel_path)

# WebDriver 종료
driver.quit()
