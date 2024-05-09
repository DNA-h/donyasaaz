import re
import logging
import requests
from selenium.common.exceptions import NoSuchElementException
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
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        response.encoding = 'utf8'
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
        div = soup.find("div", attrs={"class": "price-wrp"})
        if div is None:
            return -1
        p = div.find_all("span", attrs={"class": "woocommerce-Price-amount amount"})
        if len(p) == 0:
            return -1
        elif len(p) == 1:
            a = convert_to_english(p[0].text.strip())
        else:
            a = convert_to_english(p[1].text.strip())
        b = a
        return b
    else:
        return -1
    # try:
    #     chrome_options = Options()
    #     #chrome_options.add_argument("--headless")
    #     #chrome_options.add_argument('--no-sandbox')
    #     chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    #     # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
    #     # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)
    #     sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
    #     driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
    #                               options=chrome_options)
    #
    #     driver.set_page_load_timeout(40)
    #     driver.get(link.url)
    #
    #     # WOOCOMMERCE PRO PLUS
    #     cart = driver.find_elements(By.CSS_SELECTOR, "form.cart .single_add_to_cart_button")
    #     if cart:
    #         elements = driver.find_elements(By.CSS_SELECTOR, '.price-wrp')
    #         for element in elements:
    #             try:
    #                 # simple product
    #                 first_ins = element.find_element(By.TAG_NAME, 'ins')
    #                 if first_ins:
    #                     first_strong = first_ins.find_element(By.TAG_NAME, 'bdi')
    #                     price_text = first_strong.text.strip()
    #                     price_text = convert_to_english(price_text)
    #                     if price_text != "":
    #                         price_text = int(price_text)
    #                         driver.quit()
    #                         return price_text
    #                     else:
    #                         driver.quit()
    #                         return -1
    #                 else:
    #                     driver.quit()
    #                     return -1
    #             except NoSuchElementException:
    #                 # variation-product
    #                 # <ins> element is not available
    #                 first_strong = element.find_element(By.TAG_NAME, 'bdi')
    #                 price_text = first_strong.text.strip()
    #                 price_text = convert_to_english(price_text)
    #                 if price_text != "":
    #                     price_text = int(price_text)
    #                     driver.quit()
    #                     return price_text
    #                 else:
    #                     driver.quit()
    #                     return -1
    #
    #         driver.quit()
    #         return -1
    #     else:
    #         driver.quit()
    #         return -1
    #
    # except Exception as e:
    #     print(e)
    #     logger = logging.getLogger(__name__)
    #     logger.info('%s :  %s,', site, e)
    #     return None


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

    return converted_text;

#
# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://sazkala.com/product/yamaha-yh-e500a/")
# print(sazkala(item, None, None))
#
# item = MyObject("https://sazkala.com/product/ltd-mt-130-orange/")
# print(sazkala(item, None, None))