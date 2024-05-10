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
import time


def atikalamarket(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")

        chrome_options.add_argument('--blink-settings=imagesEnabled=false')

        # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
        # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)

        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                             options=chrome_options)

        driver.set_page_load_timeout(40)
        driver.get(link.url)

        # CUSTOM
        try:
            elements = driver.find_elements(By.CSS_SELECTOR,  ".price .ywcrbp_sale_price  bdi")
            final_price = -1
            for element in elements:
                    price_text = element.text.strip()
                    price_text = convert_to_english(price_text)
                    if price_text != "":
                        price_text = int(price_text)
                        if final_price > 0 and price_text < final_price:
                            final_price = price_text
                        else:
                            if final_price == -1:
                                final_price = price_text
            driver.quit()
            return final_price

        except NoSuchElementException:
            driver.quit()
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
# item = MyObject("https://www.atikalamarket.com/Product/AKP-25554/%D9%BE%DB%8C%D8%A7%D9%86%D9%88-%D8%AF%DB%8C%D8%AC%DB%8C%D8%AA%D8%A7%D9%84-%D9%85%D8%AF%D9%84-%D8%B1%D9%88%D9%84%DB%8C-49k/")
# print(atikalamarket(item, None, None))
