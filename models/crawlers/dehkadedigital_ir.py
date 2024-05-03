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

def dehkadedigital(link, headers, site):
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


        cart = driver.find_elements(By.CSS_SELECTOR, ".single_add_to_cart_button")
        if cart:
            elements = driver.find_elements(By.CSS_SELECTOR, '.summary.entry-summary')
            for element in elements:
                try:
                    # simple product
                    first_ins = element.find_element(By.TAG_NAME, 'ins')
                    if first_ins:
                        first_strong = first_ins.find_element(By.CSS_SELECTOR, '.amount')
                        price_text = first_strong.text.strip()
                        price_text = convert_to_english(price_text)
                        if price_text != "":
                            price_text = int(price_text)
                            driver.close()
                            return price_text
                        else:
                            driver.close()
                            return -1
                    else:
                        driver.close()
                        return -1
                except NoSuchElementException:
                    # variation-product
                    # <ins> element is not available
                    first_strong = element.find_element(By.CSS_SELECTOR, '.amount')
                    price_text = first_strong.text.strip()
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
# item = MyObject("https://dehkadedigital.ir/product/%d9%be%d8%ae%d8%b4-%da%a9%d9%86%d9%86%d8%af%d9%87-%d8%a8%db%8c-%d8%b3%db%8c%d9%85-%d9%be%d8%b1%d8%aa%d8%a7%d8%a8%d9%84-%d8%b3%d9%88%d9%86%db%8c-%d9%85%d8%af%d9%84-gtk-pg10/")
# print(dehkadedigital(item, None, None))
