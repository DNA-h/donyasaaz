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


def turborayan(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
        # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)

        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                             options=chrome_options)

        driver.set_page_load_timeout(40)
        driver.get(link.url)

        cart = driver.find_elements(By.CSS_SELECTOR, "#add_to_cart")
        if cart:
            elements = driver.find_elements(By.CSS_SELECTOR, '.our_price_display')
            for element in elements:
                try:
                    first_ins = element.find_element(By.CSS_SELECTOR, '#our_price_display')
                    if first_ins:

                        price_text = first_ins.text.strip()
                        price_text = convert_to_english(price_text)
                        if price_text != "":
                            price_text = int(int(price_text) / 10)
                            driver.quit()
                            return price_text
                        else:
                            driver.quit()
                            return -1
                    else:
                        driver.quit()
                        return -1
                except NoSuchElementException:
                    driver.quit()
                    return -1

            driver.quit()
            return -1
        else:
            driver.quit()
            return -1

    except Exception as e:
        print(e)
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

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
# item = MyObject("https://turborayan.com/%D9%85%DB%8C%DA%A9%D8%B1%D9%88%D9%81%D9%88%D9%86/26002-saramonic-uwmic9-tx-xlr9.html")
# print(turborayan(item, None, None))