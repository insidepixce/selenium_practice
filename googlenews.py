from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import re


chromedriver_path = "/Users/inseoulmate/Downloads/chromedriver-mac-arm64/chromedriver"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

articles = []
page = 1

while page <= 60:  # Limit data collection to 60 pages
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page={page}"
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sh_text")))
    article_number = (page - 1) * 30 + 1
    news_items = driver.find_elements(By.CLASS_NAME, "sh_text")

    for item in news_items:
        try:
            press = item.find_element(By.CLASS_NAME, "sh_text_press").text
        except:
            press = ""

        try:
            headline = item.find_element(By.CLASS_NAME, "sh_text_headline").text
        except:
            headline = ""

        try:
            preview = item.find_element(By.CLASS_NAME, "sh_text_lede").text
        except:
            preview = ""

        try:
            link = item.find_element(By.CLASS_NAME, "sh_text_headline").get_attribute("href")
        except:
            link = ""

        article = {
            "번호": article_number,
            "언론사": press,
            "기사 제목": headline,
            "미리보기 내용": preview,
            "기사 링크": link
        }
        articles.append(article)
        article_number += 1

    # Check if the "헤드라인 더보기" button is present on the page
    more_button = driver.find_element(By.XPATH, "//a[contains(@class, 'cluster_more_inner')]")
    if "more" in more_button.get_attribute("class"):
        # Click the "헤드라인 더보기" button using JavaScript to bypass element intercept
        driver.execute_script("arguments[0].click();", more_button)
        page += 1
    else:
        # If the "헤드라인 더보기" button is not present, exit the loop
        break

driver.quit()
text = " ".join([article["기사 제목"] + " " + article["미리보기 내용"] for article in articles])
def extract_keywords(text, num_top_keywords=10):
    words = re.findall(r'\w+', text.lower())
    counter = collections.Counter(words)
    return counter.most_common(num_top_keywords)
top_keywords = extract_keywords(text, num_top_keywords=10)
print("가장 많이 나온 키워드 Top 10:")
for keyword, count in top_keywords:
    print(f"{keyword}: {count}회")
print("\n기사 목록:")
for article in articles:
    print(f"{article['번호']}. {article['언론사']} - {article['기사 제목']} ({article['기사 링크']})")
keywords_str = "가장 많이 나온 키워드 Top 10:\n"
for keyword, count in top_keywords:
    keywords_str += f"{keyword}: {count}회\n"
with open("top_keywords.txt", "w", encoding="utf-8") as file:
    file.write(keywords_str)
articles_str = "기사 목록:\n"
for article in articles:
    articles_str += f"{article['번호']}. {article['언론사']} - {article['기사 제목']} ({article['기사 링크']})\n"
with open("articles_list.txt", "w", encoding="utf-8") as file:
    file.write(articles_str)
