import re
import logging
import sys

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def t2fungallery(link, headers, site):
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--follow-redirects")

        # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
        # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)

        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)

        driver.set_page_load_timeout(40);driver.get(link.url);

        # FIXED WOOCOMMERCE
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, '.seller-box')
            for element in elements:
                span = element.find_element(By.CSS_SELECTOR, '.item-newprice')
                price_text = span.text.strip()
                price_text = convert_to_english(price_text)
                if price_text != "":
                    price_text = int(price_text)
                    driver.close()
                    return price_text
                else:
                    driver.close()
                    return -1
            driver.close()
            return -1
        except NoSuchElementException:
            driver.close()
            return -1

    except Exception as ee:
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


# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://2fungallery.ir/product/119/%D8%B3%D8%A7%D8%B2-%DA%A9%D8%A7%D9%84%DB%8C%D9%85%D8%A8%D8%A7-%DB%B1%DB%B7-%D8%AA%DB%8C%D8%BA%D9%87-%D8%B6%D8%AF%D8%B2%D9%86%DA%AF-%DA%86%D9%88%D8%A8-%DA%AF%D8%B1%D8%AF%D9%88/?utm_medium=PPC&utm_source=Torob")
# print(t2fungallery(item, None, None))
