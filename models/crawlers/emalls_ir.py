import re
import logging
import sys

from selenium.webdriver.common.by import By
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


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

def emalls(link, headers, site):
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

        # Find the element containing the product price
        elements = driver.find_elements(By.CSS_SELECTOR, 'h2 ~ .price-more')

        if elements is not None:
            for element in elements:

                strong_element = element.find_element(By.TAG_NAME, 'strong')
                if strong_element:
                    first_strong = strong_element
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
            driver.close()
            return -1
        driver.close()
        return -1
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None





# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://emalls.ir/%d9%85%d8%b4%d8%ae%d8%b5%d8%a7%d8%aa_%da%af%db%8c%d8%aa%d8%a7%d8%b1-%d9%81%d9%84%d8%a7%d9%85%d9%86%da%a9%d9%88-Alhambra-%d9%85%d8%af%d9%84-4F-%d8%b3%d8%a7%db%8c%d8%b2-4-4~id~182315")
# print(emalls(item, None, None))
