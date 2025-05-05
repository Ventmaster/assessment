# By Eashan Srivastava
# Email: eashan455@gmail.com

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator
from collections import Counter

import requests
import re
import time
import os

# Create a folder to save images
os.makedirs("images", exist_ok=True)

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Open El Pais
print("Opening elpais.com...")
driver.get("https://elpais.com/")
# time.sleep(5)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Opinión"))
)

# Step 2: Navigate to 'Opinión' Section
print("Navigating to 'Opinión' section...")
opinion_link = driver.find_element(By.LINK_TEXT, "Opinión")
opinion_link.click()
# time.sleep(5)
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
)

# Step 3: Scrape Articles
print("Extracting first 5 articles...")
articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
article_data = []

for i, article in enumerate(articles):
    print(f"\nProcessing article {i+1}...")
    try:
        title_elem = article.find_element(By.CSS_SELECTOR, "h2 a")
        title = title_elem.text
        link = title_elem.get_attribute("href")

        print(f"  Title: {title}")
        print(f"  Link: {link}")

        # Visit the article page
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(3)

        # Extract article content
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
        content = "\n".join([p.text for p in paragraphs if p.text.strip()])

        # print(f"  Content Extracted. First 100 chars: {content[:100]}...")

        snippet_es = content[:100]
        snippen_en = GoogleTranslator(source = 'es', target = 'en').translate(snippet_es)

        print(f"  Content Snippet (ES): {snippet_es}:")
        print(f"  Content Snippet (EN): {snippen_en}:")

        # Extract image
        try:
            image_elem = driver.find_element(By.CSS_SELECTOR, "figure img")
            img_url = image_elem.get_attribute("src")

            if img_url:
                img_data = requests.get(img_url).content
                image_filename = f"images/article_{i+1}.jpg"
                with open(image_filename, "wb") as f:
                    f.write(img_data)
                print(f"  Cover Image Saved: {image_filename}")
            else:
                print("  No Image Found.")
        except Exception as e:
            print("  No Image Found.")

        # Save data
        article_data.append({
            "title": title,
            "content": content,
            "link": link
        })

        # Close article tab and return
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"  Error processing article {i+1}: {e}")

driver.quit()

# Step 4: Translate Titles
print("\nTranslating Titles...")
translated_titles = []
for article in article_data:
    translated_title = GoogleTranslator(source='es', target='en').translate(article["title"])
    translated_titles.append(translated_title)
    print(f"Original: {article['title']} | Translated: {translated_title}")

# Step 5: Analyze Repeated Words
print("\nAnalyzing Translated Titles for Repeated Words...")
all_words = " ".join(translated_titles).lower()
all_words = re.findall(r'\b\w+\b', all_words)

word_counts = Counter(all_words)
repeated_words = {word: count for word, count in word_counts.items() if count > 2}

print("\nRepeated Words (more than twice):")
for word, count in repeated_words.items():
    print(f"{word}: {count}")

# Ready for BrowserStack Parallel Execution
print("\nScript completed successfully!")

# Running the test
username = "mai_nahi_bataunga" 
pwd = "mai_nahi_bataunga"

# different browser configurations
BROWSER_CONFIGS = [
    {"browserName": "Chrome", "browserVersion": "latest", "os": "Windows", "osVersion": "10"},
    {"browserName": "Firefox", "browserVersion": "latest", "os": "Windows", "osVersion": "10"},
    {"browserName": "Edge", "browserVersion": "latest", "os": "Windows", "osVersion": "10"},
    {"browserName": "Safari", "browserVersion": "latest", "os": "OS X", "osVersion": "Monterey"},
    {"browserName": "Chrome", "browserVersion": "latest", "device": "Samsung Galaxy S21", "realMobile": "true"}
]

# Function to run the browser tests on
def func(browser_config):
    options = webdriver.ChromeOptions()
    options.set_capability("bstack:options", browser_config)

    driver = webdriver.Remote(
        command_executor=f"https://{username}:{pwd}@hub-cloud.browserstack.com/wd/hub",
        options=options
    )

    try:
        print(f"\nTesting on {browser_config['browserName']} {browser_config.get('browserVersion', '')} on {browser_config['os']} {browser_config.get('osVersion', '')} {browser_config.get('device', '')}...")
        driver.get("https://elpais.com/opinion/")
        print("  Opened elpais.com/opinion/")
        articles = driver.find_elements(By.CSS_SELECTOR, "h2")[:5]

        if articles:
            print("Found the following article titles:")
            for article in articles:
                print(f"  [{browser_config['browserName']}] {article.text}")
        else:
            print("Can't find any titles.")

    except Exception as e:
        print(f"An error occurred during testing on {browser_config['browserName']}: {e}")

    finally:
        print(f"Closing the browser on {browser_config['browserName']}.")
        driver.quit()

# Use a thread pool to run the browser tests parallely
print("Initiating BrowserStack tests...")
with ThreadPoolExecutor(max_workers=len(BROWSER_CONFIGS)) as executor:
    executor.map(func, BROWSER_CONFIGS)

print("TASK COMPLETED")
print("THANK YOU!");
