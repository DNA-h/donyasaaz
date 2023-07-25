import re
import logging
import sys
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import math


def gostaresh(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
        # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)
        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        elements = driver.find_elements(By.CSS_SELECTOR,'.footer-product.hidden-xs .product-page__prices')
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if elements:
        for element in elements:
            try:
                prices = element.find_elements(By.TAG_NAME, "div")
                for div in prices:
                    if "old-price" not in div.get_attribute("class"):
                        final_div = div
                    else:
                        final_div = div.find_elements(By.TAG_NAME, "div")
                        final_div = final_div[0]
                    price_text = final_div.text.strip()
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
    else:
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


# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://www.gostaresh-seda.com/%D9%85%D8%AD%D8%B5%D9%88%D9%84/2118/focusrite-scarlett-4i4-3rd-gen")
# print(gostaresh(item, None, None))
