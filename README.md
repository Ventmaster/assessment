# Assessment - Round 2

## Overview

The core objective is to demonstrate competence in web automation, data retrieval, language processing, and cross-browser compatibility testing.

## Project Structure

The repository contains the following file:
-   `test.py`: The primary Python script, encompassing all the logic. 

## Dependencies

The project relies on the following Python libraries.  These can be installed using pip:

```bash
pip install selenium webdriver-manager deep-translator requests collections

Collections which provides the Counter class, used to tally word frequencies.
Deep Translator for translating text between languages (Spanish to English in this case).
Requests for making HTTP requests to download images.
Selenium for automating web browser interactions.
WebDriverManager to automate the management of browser drivers

Execution
To execute the script, ensure the required dependencies are installed and you have a stable internet connection. Run the script from your terminal:
python test.py


The script will proceed with these actions:
1. Web Scraping: Open the El País website, navigate to the "Opinión" section, and extract the titles, links, initial content (the first 5 paragraphs), and image URLs from the first 5 articles.
2. Image Downloading: Download the images associated with the extracted articles, saving them as article_1.jpg, article_2.jpg, and so on.
3. Title Translation: Translate the titles of the extracted articles from Spanish to English. Both the original and translated titles are then printed to the console.
4. Content Translation: Translate the initial content (first 5 paragraphs) of the extracted articles from Spanish to English. The translated content is printed.
5. Word-frequency Analysis: Analyze the translated article titles to identify words that appear more than twice. The frequency of these words is then displayed.
6. Cross-Browser Testing: Access the El País "Opinión" page in a set of pre-defined browser configurations, using a remote testing service. The titles of the first 5 articles, as rendered in each browser environment, are printed.

Observations
1. This script uses pauses (time.sleep()) to ensure that web pages are fully loaded before attempting to interact with their elements. This helps prevent common errors related to asynchronous page loading.
2. Error handling (try...except blocks) is used to manage potential exceptions during the web scraping process, such as elements not being found/network connectivity issues.
3. Content extraction is limited to the first 5 paragraphs of each article. This was done to keep the processing load reasonable.
4. The word-frequency analysis focuses on words appearing more than twice in the translated titles.
5. Cross-browser testing is conducted across a set of common browsers and operating systems to demonstrate compatibility.

```
Created by: Eashan Srivastava,
Email ID: eashan455@gmail.com

THANK YOU! 
