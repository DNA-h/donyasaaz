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
        # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
        # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)

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
        elements = elements[0:4]
        smallest = 0

        for price_element in elements:
            # Extract the price text
            price_text_orig = price_element.text.strip()
            price_text = convert_to_english(price_text_orig)

            if price_text != "" and "ناموجود" not in price_text_orig:
                price_text = int(price_text)
            else:
                price_text = 0
            if smallest > 0:
                if smallest > price_text > 0:
                    smallest = price_text
            else:
                smallest = price_text
        if smallest > 0:
            return smallest
        else:
            return -1




# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://torob.com/p/8e5ab0d6-4ea7-4774-9b9f-d71fb1da4061/%D9%BE%DB%8C%D8%A7%D9%86%D9%88-%D8%AF%DB%8C%D8%AC%DB%8C%D8%AA%D8%A7%D9%84-%D8%B1%D9%88%D9%84%D9%86%D8%AF-%D9%85%D8%AF%D9%84-rp30/")
# print(torob(item, None, None))