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


def violinkadeh(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
        # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)

        sys.path.append("C:\\Users\\USER\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\USER\\donyasaaz\\chromedriver.exe",
                             options=chrome_options)

        driver.get(link.url)


        try:
            out_stock = driver.find_element(By.CSS_SELECTOR, ".status div")
            text_status = out_stock.text.strip()

            if text_status == "ناموجود در انبار":
                driver.close()
                return -1
            else:
                elements = driver.find_elements(By.CSS_SELECTOR, ".price-add-to-cart .price.d-flex")
                for element in elements:
                    ins = element.find_element(By.TAG_NAME, 'ins')
                    bdi = ins.find_element(By.TAG_NAME, 'bdi')
                    price_text = bdi.text.strip()
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
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, '.price-add-to-cart .price')
                if elements:
                    for element in elements:
                        bdi = element.find_element(By.TAG_NAME, 'bdi')
                        price_text = bdi.text.strip()

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
                else:
                    driver.close()
                    return -1
            except NoSuchElementException as e:
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
# item = MyObject("http://violinkadeh.com/product/%d9%87%d8%af%d9%81%d9%88%d9%86-%d8%a8%db%8c%d8%b1%d8%af%d8%a7%db%8c%d9%86%d8%a7%d9%85%db%8c%da%a9-dt-1770-pro/")
# print(violinkadeh(item, None, None))
