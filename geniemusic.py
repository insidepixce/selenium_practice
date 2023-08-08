from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "/Users/inseoulmate/Downloads/chromedriver-mac-arm64/chromedriver"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)


driver.get("https://www.genie.co.kr/chart/top200")


wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list-wrap")))

chart_items = driver.find_elements(By.CSS_SELECTOR, ".list-wrap > tbody > tr.list")

for item in chart_items:
    rank = item.find_element(By.CLASS_NAME, "number").text
    title = item.find_element(By.CSS_SELECTOR, ".info .title").text
    artist = item.find_element(By.CSS_SELECTOR, ".info .artist").text

    print(f"{title} - {artist}")

# 셀레니움 웹 드라이버 종료
driver.quit()
