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


def walkala(link, headers, site):
    try:
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--follow-redirects")
        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.set_page_load_timeout(40);driver.get(link.url);

        # FIXED WOOCOMMERCE
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, '.price')
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
                elements = driver.find_elements(By.CSS_SELECTOR, '.price')
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
#
# item = MyObject("https://walkala.com/product/%d9%87%d8%a7%d8%b1%d8%af-%d8%af%db%8c%d8%b3%da%a9-hdd-%d8%a8%d8%b1%d9%86%d8%af-western-digital-%d9%85%d8%af%d9%84-wd10ezex-%d8%b8%d8%b1%d9%81%db%8c%d8%aa-1-%d8%aa%d8%b1%d8%a7%d8%a8%d8%a7%db%8c/")
# print(walkala(item, None, None))
