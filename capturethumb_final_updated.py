from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.request
import os
import re
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import ssl
import time 
from PIL import Image

ssl._create_default_https_context = ssl._create_unverified_context

def safe_create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(filename):
    s = re.sub(r'[\\/*?:"<>|]', "", filename)
    return s.strip()

# Initialize

# Initialize
search_query = input("검색어를 입력하세요: ")
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)
driver.implicitly_wait(10)

# Wait for loading
time.sleep(5)

# Open YouTube and input search query
driver.get("https://www.youtube.com/")

# Wait for loading
time.sleep(5)

search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
search_box.clear()
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# Wait for loading
time.sleep(5)

scroll_pause_time = 2
last_height = driver.execute_script("return document.documentElement.scrollHeight")
target_video_count = 10

video_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
data = []

while len(data) < target_video_count:
    video_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
    
    if not video_elements:
        # Scroll to load more videos
        print("썸네일을 가져올 수 없어 스크롤합니다")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        try:
            wait.until(EC.presence_of_element_located((By.ID, "continuations")))
        except TimeoutException:
            break
        time.sleep(scroll_pause_time)
        continue

    for video in video_elements:
        title = video.find_element(By.ID, "video-title").text
        sanitized_title = sanitize_filename(title)
        
        try:
            uploader_element = video.find_element(By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.yt-formatted-string")
            uploader = uploader_element.text
        except NoSuchElementException:
            uploader = "알 수 없는 업로더"
        
        views = video.find_elements(By.CSS_SELECTOR, "span.style-scope.ytd-video-meta-block")[0].text

        # 이미지 요소가 yt-img 클래스 안에 있을 수 있으므로 yt-img 클래스를 포함한 요소를 찾는다
        try:
            thumbnail_img_element = video.find_element(By.CSS_SELECTOR, "yt-img img")
            thumbnail_src = thumbnail_img_element.get_attribute("src")
            
            if thumbnail_src:
                thumbnail_folder = f"movies/{search_query}/Thumbnail/"
                safe_create_directory(thumbnail_folder)
                thumbnail_path = f"{thumbnail_folder}{sanitized_title}.jpg"
                urllib.request.urlretrieve(thumbnail_src, thumbnail_path)
                print(f"('{title}'의 '{thumbnail_path}/{sanitized_title}/{uploader}/{views}' )를 저장했습니다")
            else:
                print(f"('{title}')의 썸네일을 가져올 수 없습니다")
            
            data.append([title, uploader, views, thumbnail_path])

        except NoSuchElementException:
            print(f"('{title}'의 썸네일을 가져올 수 없습니다")

    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    try:
        wait.until(EC.presence_of_element_located((By.ID, "continuations")))
    except TimeoutException:
        break
    time.sleep(scroll_pause_time)

info_folder = f"movies/{search_query}/INFO/"
safe_create_directory(info_folder)
info_file_path = f"{info_folder}{search_query}.txt"

with open(info_file_path, "w", encoding="utf-8") as info_file:
    for item in data:
        info_file.write(f"Title: {item[0]}\n")
        info_file.write(f"Uploader: {item[1]}\n")
        info_file.write(f"Views: {item[2]}\n")
        info_file.write(f"Thumbnail: {item[3]}\n\n")

df = pd.DataFrame(data, columns=["Title", "Uploader", "Views", "Thumbnail"])

excel_folder = f"movies/{search_query}_excel/"
safe_create_directory(excel_folder)
excel_path = f"{excel_folder}{search_query}.xlsx"

workbook = pd.ExcelWriter(excel_path, engine='xlsxwriter')
df.to_excel(workbook, index=False, sheet_name='Videos')

workbook = workbook.book
worksheet = workbook.get_worksheet_by_name('Videos')

max_row = df.shape[0]
max_col = df.shape[1]

worksheet.set_column('E:E', 20)

for row_num in range(1, max_row + 1):
    image_path = df.loc[row_num - 1, 'Thumbnail']
    worksheet.insert_image(row_num, max_col, image_path, {'x_scale': 0.5, 'y_scale': 0.5})

workbook.close()

print(f"모든 데이터가 저장되었습니다. 엑셀 파일 경로: {excel_path}")

# Close browser
driver.quit()