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
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')
        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe", options=chrome_options)
        driver.get(link.url)
        # Find the element containing the product price
        elements = driver.find_elements(By.CSS_SELECTOR, '.itemprice')
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

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


# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://emalls.ir/%D9%85%D8%B4%D8%AE%D8%B5%D8%A7%D8%AA_%D8%B3%D9%86%D8%AA%D9%88%D8%B1-%D9%85%D9%88%D8%B3%D9%88%DB%8C-%D8%AF%D9%88-%D9%85%D9%87%D8%B1~id~4619479")
# print(arasound(item, None, None))
