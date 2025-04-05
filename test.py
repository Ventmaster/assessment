# Technical Assessment - Round 2
# By Eashan Srivastava
# Email: eashan455@gmail.com

# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator
from collections import Counter

import requests
import re
import time

# Setting up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigating to the requested website
print("Opening elpais.com...")
driver.get("https://elpais.com/")
time.sleep(5)  # a few seconds to load

print("Navigating to the 'Opinión' section...")
opinion_link = driver.find_element(By.LINK_TEXT, "Opinión")
opinion_link.click()
time.sleep(5)  # few seconds to loads as well

# Extracting articles, titles, links, etc.
print("Extracting data from the first 5 articles...")
articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
article_data = []

for i, article in enumerate(articles):
    print(f"Processing article {i+1}...")
    try:
        title = article.find_element(By.TAG_NAME, "h2").text
        link = article.find_element(By.TAG_NAME, "a").get_attribute("href")

        print(f"  Title: {title}")
        print(f"  Link: {link}")

        print(" Navigating to the article...")
        driver.get(link)
        time.sleep(5)

        print("  Extracting content...")
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
        # Taking text from first 5 paragraphs
        content = " ".join([p.text for p in paragraphs[:5]])

        print("Image?")
        try:
            image = driver.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            print(f"  Image URL: {image}")
        except:
            image = None
            print("No image here.")

        article_data.append({
            "Title": title,
            "Content": content,
            "Image": image,
            "Link": link
        })

    except Exception as e:
        print(f" Error encountered while processing: {e}")

    finally:
        print("Going back to the Opinions tab...")
        driver.back()
        time.sleep(5)

print("Closing the browser...")
driver.quit()

# IMAGES
print("\n--- Downloading Images ---")
for i, article in enumerate(article_data):
    if article["Image"]:
        print(f"Downloading image for article {i+1}...")
        try:
            response = requests.get(article["Image"])
            response.raise_for_status()  # Execption

            with open(f"article_{i+1}.jpg", "wb") as file:
                file.write(response.content)

            print(f"  Successfully downloaded: article_{i+1}.jpg")

        except requests.exceptions.RequestException as e:
            print(f"  Error downloading image for article {i+1}: {e}")
    else:
        print(f"Article {i+1} has no image to download.")

# ESPANOL TO ENGLISH!  
print("\n--- Translating Titles ---")
def translate_titles(titles):
    translator = GoogleTranslator(source='es', target='en')
    return [translator.translate(title) for title in titles]

original_titles = [article["Title"] for article in article_data]
translated_titles = translate_titles(original_titles)

# Espanol to English continue. 
for original, translated in zip(original_titles, translated_titles):
    print(f"Original (Spanish): {original}")
    print(f"Translation (English): {translated}\n")

print("\n--- Translating Content ---")
def translate_content(contents):
    translator = GoogleTranslator(source='es', target='en')
    return [translator.translate(content) for content in contents]

original_contents = [article["Content"] for article in article_data]
translated_contents = translate_content(original_contents)

for i, translated in enumerate(translated_contents):
    print(f"Translated Content {i+1} (English):\n{translated}\n")

# Word-frequency analysis
print("\n--- Word Frequency Analysis of Titles ---")
def analyze_titles(translated_titles):
    all_words = []
    for title in translated_titles:
        # Spliting the title into words and converting it to lowercase
        words = re.findall(r'\b\w+\b', title.lower())
        all_words.extend(words)

    # Count the occurrences of each word
    word_count = Counter(all_words)

    # As per the condition i.e if word repetition >=2 
    repeated_words = {word: count for word, count in word_count.items() if count > 2}

    # sorting by frequency
    return dict(sorted(repeated_words.items(), key=lambda item: item[1], reverse=True))

repeated_words = analyze_titles(translated_titles)
print("Repeated Words Across The Translated Titles:")
if repeated_words:
    for word, count in repeated_words.items():
        print(f"{word}: {count}")
else:
    print("No words appear more than twice.")

# Running the test
username = "eashansrivastava_fWgx54"
pwd = "HQyy2kRF5mv8z5VickFF"

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