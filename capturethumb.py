from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# 검색어 입력 받기
search_query = input("검색어를 입력하세요: ")

# 크롬 드라이버의 옵션들을 설정
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# 크롬 드라이버 초기화
driver = Chrome(options=chrome_options)

# 웹드라이버 초기화
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(5)
driver.maximize_window()

# 유튜브 사이트 열기
driver.get("https://www.youtube.com/")

# 검색어 입력
search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# 검색 결과 기다리기
wait.until(EC.presence_of_element_located((By.ID, "contents")))

# 검색 결과 썸네일 및 정보 스크래핑
video_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
for video in video_elements:
    title = video.find_element(By.ID, "video-title").text
    preview = video.find_element(By.CSS_SELECTOR, "yt-img-shadow img").get_attribute("src")
    uploader = video.find_element(By.ID, "text").text
    views = video.find_element(By.CSS_SELECTOR, "span.style-scope.ytd-video-meta-block").text
    
    # 썸네일 저장
    thumbnail_url = f"movies/{search_query}/thumbnails/{title}.jpg"
    thumbnail_element = video.find_element(By.CSS_SELECTOR, "yt-img-shadow img")
    thumbnail_src = thumbnail_element.get_attribute("src")
    urllib.request.urlretrieve(thumbnail_src, thumbnail_url)
    
    # 정보 저장
    info_file_path = f"movies/{search_query}_info/{title}.txt"
    with open(info_file_path, "w") as info_file:
        info_file.write(f"Title: {title}\n")
        info_file.write(f"Preview: {preview}\n")
        info_file.write(f"Uploader: {uploader}\n")
        info_file.write(f"Views: {views}\n")

# 브라우저 종료
driver.quit()
