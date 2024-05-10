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


def alfamark(link, headers, site):
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

        cart = driver.find_elements(By.CSS_SELECTOR, ".product-buy-add-to-list")
        if cart:
            elements = driver.find_elements(By.CSS_SELECTOR, '#product-buy-content-price-price')
            for element in elements:
                try:

                    price_text = element.text.strip()
                    price_text = convert_to_english(price_text)
                    if price_text != "":
                        price_text = int(price_text)
                        driver.quit()
                        return price_text
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
# item = MyObject("https://alfamark.ir/product.php?link=%D9%85%DB%8C%DA%A9%D8%B1%D9%88%D9%81%D9%86_%D8%AF%DB%8C%D9%86%D8%A7%D9%85%DA%A9%DB%8C_%DB%8C%D9%88_%D8%A7%D8%B3_%D8%A8%DB%8C_%D8%B4%D9%88%D8%B1_Shure_Mv7_Podcast_Microphone_Professional_USb_Compatible_For_Pc&id=54629&utm_medium=PPC&utm_source=Torob")
# print(alfamark(item, None, None))