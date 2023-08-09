from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# 검색어 입력 받기
search_query = input("검색어를 입력하세요: ")

# 크롬 드라이버의 옵션들을 설정
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# 크롬 드라이버 초기화
driver = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 웹드라이버 초기화
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(5)
driver.maximize_window()

# 유튜브 사이트 열기
driver.get("https://www.youtube.com/")

# 검색어 입력 및 검색
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys(search_query)

# 검색 버튼 클릭
search_button = driver.find_element(By.ID, "search-icon-legacy")
search_button.click()

# 검색 결과가 로딩될 때까지 대기
wait.until(EC.presence_of_element_located((By.ID, "video-title")))

# 스크린샷 캡쳐
screenshot_path = "youtube"
if not os.path.exists(screenshot_path):
    os.mkdir(screenshot_path)

screenshot_filename = f"{search_query}_on_youtube.png"
screenshot_full_path = os.path.join(screenshot_path, screenshot_filename)

driver.save_screenshot(screenshot_full_path)
print(f"스크린샷이 '{screenshot_full_path}'에 저장되었습니다.")

# 드라이버 종료
driver.quit()
