import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
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


def ertebat(link, headers, site):
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--follow-redirects")
        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe", options=chrome_options)
        driver.set_page_load_timeout(40);driver.get(link.url);

        # FIXED WOOCOMMERCE
        try:
            elements = driver.find_elements(By.ID, "hikashop_product_price_main")
            if elements:
                for element in elements:
                    item_price = element.find_element(By.CSS_SELECTOR, ".hikashop_product_price")
                    price_text = item_price.text.strip()
                    price_text = convert_to_english(price_text)
                    if price_text != "":
                        price_text = price_text[:-1]
                        price_text = int(price_text)
                        driver.close()
                        return price_text
                    else:

                        driver.close()
                        return -1
                driver.close()
                return -1
            else:

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
# item = MyObject("https://ertebat.co/product/sennheiser_ew_135-p_g3")
# print(ertebat(item, None, None))

