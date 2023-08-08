
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
#크롬 드라이버 자동업데이를 위함
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
#브라우저가 자동으로 꺼질 경우 방지 코드 
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
#크롬 드라이버 최신 버전을 설치 후 서비스 객체를 만듦
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
#웹페이지 오픈을 위한 옵션들
driver.implicitly_wait(5)
driver.maximize_window()
#웹페이지 주소로 이동
driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/')
#아이디 입력
id = driver.find_element(By.CSS_SELECTOR, '#id')
id.click()
pyperclip.copy('insidepixce')
id.send_keys(Keys.CONTROL, 'v')
time.sleep(2)

#비밀번호 입력
pw = driver.find_element(By.CSS_SELECTOR, '#pw')
pw.click()
pyperclip.copy('p8152005!')

pw.send_keys(Keys.CONTROL, 'v')
time.sleep(2)
login_btn  = driver.find_element(By.CSS_SELECTOR, '#log\.login')
login_btn.click()
