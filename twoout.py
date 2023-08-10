from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from PIL import Image
from io import BytesIO
import os

# 검색어 입력
search_query = input("검색어를 입력하세요: ")

# Selenium WebDriver 설정
driver = webdriver.Chrome()
driver.get("https://www.youtube.com/results?search_query=" + search_query)

# 썸네일 요소들 찾기
thumbnail_elements = driver.find_elements(By.CSS_SELECTOR, "a#thumbnail yt-image img")

# 캡처한 이미지 저장할 디렉토리 생성
save_directory = f"movies/{search_query}"
os.makedirs(save_directory, exist_ok=True)

# 각 썸네일 요소마다 이미지 캡처 및 저장
for index, thumbnail_element in enumerate(thumbnail_elements):
    thumbnail_url = thumbnail_element.get_attribute("src")
    
    if thumbnail_url:
        response = requests.get(thumbnail_url)
        thumbnail = Image.open(BytesIO(response.content))
        
        # 파일명을 index 기반으로 생성
        save_path = os.path.join(save_directory, f"{index + 1}.jpg")
        thumbnail.save(save_path)
    else:
        print(f"Thumbnail URL not found for index {index + 1}")

# WebDriver 종료
driver.quit()