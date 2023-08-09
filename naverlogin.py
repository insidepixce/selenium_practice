# Import necessary modules and classes from the Selenium library
from selenium.webdriver import Chrome, ChromeOptions, Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


# Configure Chrome options
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# 웹드라이버 조건 설정
driver = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 웹드라이버 초기화 
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(5)
driver.maximize_window()
#브라우저 종료 현상 방지 
chrome_options = ChromeOptions()
chrome_options.add_experimental_option('detach', True)
# Open the specified URL using the Chrome driver
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

# Find the username input field by its ID and wait until it's present, then input the username
username = wait.until(EC.presence_of_element_located((By.ID, 'id')))
username.send_keys('insidepixce')  # Replace 'your_username' with your actual username
time.sleep(10)
# Find the password input field by its ID and wait until it's present, then input the password
password = wait.until(EC.presence_of_element_located((By.ID, 'pw')))
password.send_keys('p8152005!')  # Replace 'your_password' with your actual password
time.sleep(10)
# Simulate pressing the Enter key to submit the login form
password.send_keys(Keys.ENTER)
input()