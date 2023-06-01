import re
import logging
import sys
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def convert_to_english(text):
    persian_to_english = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
        # Add more mappings for other Persian characters if needed
    }

    converted_text = ''

    for char in text:
        if char in persian_to_english:
            converted_text += persian_to_english[char]
        else:
            converted_text += char

    # Remove non-numeric characters
    converted_text = ''.join(c for c in converted_text if c.isdigit())

    return converted_text
def torob(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--log-level=3')
        sys.path.append("C:\\Users\\USER\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\USER\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        elements = driver.find_elements(By.CSS_SELECTOR, '.seller-element.price')

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if elements is not None:
        elements = elements[0:3]
        largest = 0

        for price_element in elements:
            # Extract the price text
            price_text = price_element.text.strip()
            price_text = convert_to_english(price_text)
            print(price_text)
            if price_text != "":
                price_text = int(price_text)
            else:
                price_text = 0
            if largest > 0:
                if largest > price_text > 0:
                    largest = price_text
            else:
                largest = price_text
        if largest > 0:
            return largest
        else:
            return -1
