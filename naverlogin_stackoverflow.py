from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

wait.until(EC.element_to_be_clickable((By.ID, "id"))).send_keys("insidepixce")
wait.until(EC.element_to_be_clickable((By.ID, "pw"))).send_keys("p8152005!")
wait.until(EC.element_to_be_clickable((By.ID, "log.login"))).click()

input()