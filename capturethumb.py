
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.request
import os
import re
import pandas as pd
import ssl

# Create an unverified context to bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

def safe_create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(filename):
    s = re.sub(r'[\\/*?:"<>|]', "", filename)
    return s.strip()

# Initialize
search_query = input("검색어를 입력하세요: ")
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)
driver.implicitly_wait(10)

# Open YouTube and input search query
driver.get("https://www.youtube.com/")
search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
search_box.clear()
search_box.send_keys(search_query)
search_box.submit()  # Use this line instead of search_box.send_keys(Keys.RETURN)

# Wait for search results
wait.until(EC.presence_of_element_located((By.ID, "contents")))
# Scraping
video_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")[:10]  # Limiting to top 10 results
data = []
for video in video_elements:
    title = video.find_element(By.ID, "video-title").text
    sanitized_title = sanitize_filename(title)
    
    # Get uploader element and extract uploader name
    uploader_element = video.find_element(By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.yt-formatted-string")
    uploader = uploader_element.text
    
    views = video.find_elements(By.CSS_SELECTOR, "span.style-scope.ytd-video-meta-block")[0].text
    
    # Find the thumbnail image element
    thumbnail_img = video.find_element(By.CSS_SELECTOR, "yt-image img")
    thumbnail_src = thumbnail_img.get_attribute("src")
    
    if thumbnail_src:
        # Save thumbnail
        thumbnail_folder = f"movies/{search_query}/Thumbnail/"
        safe_create_directory(thumbnail_folder)
        thumbnail_path = f"{thumbnail_folder}{sanitized_title}.jpg"
        urllib.request.urlretrieve(thumbnail_src, thumbnail_path)
        
        # Save info to a list for later excel export
        data.append([title, uploader, views, thumbnail_path])
    else:
        print(f"Thumbnail URL not found for video: {title}")

# Save info to text file
info_folder = f"movies/{search_query}/INFO/"
safe_create_directory(info_folder)
info_file_path = f"{info_folder}{search_query}.txt"
with open(info_file_path, "w", encoding="utf-8") as info_file:
    for item in data:
        info_file.write(f"Title: {item[0]}\n")
        info_file.write(f"Uploader: {item[1]}\n")
        info_file.write(f"Views: {item[2]}\n")
        info_file.write(f"Thumbnail Path: {item[3]}\n\n")

# Save to Excel
df = pd.DataFrame(data, columns=["Title", "Uploader", "Views", "Thumbnail Path"])
excel_folder = f"movies/{search_query}_excel/"
safe_create_directory(excel_folder)
excel_path = f"{excel_folder}{search_query}.xlsx"
df.to_excel(excel_path, index=False)

print(f"All data saved. Excel file path: {excel_path}")

# Close browser
driver.quit()

# Close browser
driver.quit()
