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


def sazplus(link, headers, site):
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

        # FIXED WOOCOMMERCE PRO
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, ".elementor-element-6f33617 .price")
            for element in elements:
                ins = element.find_element(By.TAG_NAME, 'ins')
                bdi = ins.find_element(By.TAG_NAME, 'bdi')
                price_text = bdi.text.strip()
                price_text = convert_to_english(price_text)
                if price_text != "":
                    price_text = int(price_text)
                    driver.quit()
                    return price_text
                else:
                    driver.quit()
                    return -1
            driver.quit()
            return -1
        except NoSuchElementException:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR,
                                                '.elementor-element-6f33617 .price')
                if elements:
                    for element in elements:
                        bdi = element.find_element(By.TAG_NAME, 'bdi')
                        price_text = bdi.text.strip()

                        price_text = convert_to_english(price_text)
                        if price_text != "":
                            price_text = int(price_text)
                            driver.quit()
                            return price_text
                        else:
                            driver.quit()
                            return -1
                    driver.quit()
                    return -1
                else:
                    driver.quit()
                    return -1
            except NoSuchElementException as e:
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
# item = MyObject("https://sazplus.com/product/%D8%A2%D9%85%D9%BE%D9%84%DB%8C-%D9%81%D8%A7%DB%8C%D8%B1-%DA%AF%DB%8C%D8%AA%D8%A7%D8%B1-%D8%A7%D9%84%DA%A9%D8%AA%D8%B1%DB%8C%DA%A9-%D9%88%DA%A9%D8%B3-%D9%85%D8%AF%D9%84-pathfinder-10/?utm_source=EmallsCompairingPrice&utm_medium=EmallsPPC&utm_campaign=Emalls")
# print(sazplus(item, None, None))
