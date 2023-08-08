from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import pyperclip
import time

from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(5)
driver.maximize_window()

driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

#ENTER ID
id= driver.find_element(By.CSS_SELECTOR, "#id")
id.click()
pyperclip.copy('insidepixce')
id.send_keys(Keys.CONTROL,'v')
time.sleep(2)

#ENTER PW
pw = driver.find_element(By.CSS_SELECTOR, "#pw")
pw.click()
pyperclip.copy('p8152005!')
pw.send_keys(Keys.CONTROL,'v')
time.sleep(2)

#CLICK LOGIN BUTTON
login_btn = driver.find_element(By.CSS_SELECTOR, "#log\.login")
login_btn.click()
