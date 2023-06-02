import re
import logging
import requests
from selenium.webdriver.common.by import By
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import sys

def sazkala(link, headers, site):
    elements = None
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        sys.path.append("C:\\Users\\USER\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\USER\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        elements = driver.find_elements(By.CSS_SELECTOR, '.price-wrp')
        driver.close()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    try:

        for element in elements:
            first_strong = element.find_element(By.TAG_NAME, 'bdi')
            if first_strong:
                price_text = first_strong.text.strip()
                price_text = convert_to_english(price_text)
                if price_text != "":
                    price_text = int(price_text)
                    return price_text
                else:
                    return -1
            else:
                return -1

        return -1

    except Exception as e:
        driver.close()
        return -1


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
