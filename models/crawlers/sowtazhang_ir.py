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


def sowtazhang(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")

        chrome_options.add_argument('--blink-settings=imagesEnabled=false')

        # sys.path.append("C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe")
        # driver = webdriver.Chrome(executable_path="C:\\MyBackups\\robot donyayesaaz\\chromedriver.exe",options=chrome_options)

        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                             options=chrome_options)

        driver.set_page_load_timeout(40);driver.get(link.url);

        # FIXED WOOCOMMERCE PRO
        try:
            cart = driver.find_elements(By.CSS_SELECTOR, ".cart .single_add_to_cart_button")
            if cart:
                try:

                    elements = driver.find_elements(By.CSS_SELECTOR, ".summary_cart_warp .price")
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
                                                        '.summary_cart_warp .price')
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
# item = MyObject("https://sowtazhang.ir/product/beyerdynamic-dt-770-pro-250-ohm/")
# print(sowtazhang(item, None, None))
#
# item = MyObject("https://sowtazhang.ir/product/%da%a9%d8%a7%d8%b1%d8%aa-%d8%b5%d8%af%d8%a7-%d8%a7%da%a9%d8%b3%d8%aa%d8%b1%d9%86%d8%a7%d9%84-%d8%a7%d8%b4%d8%aa%d8%a7%db%8c%d9%86%d8%a8%d8%b1%da%af-steinberg-ur12/")
# print(sowtazhang(item, None, None))
#
#
# item = MyObject("https://sowtazhang.ir/product/m-audio-keystation-61-mk3/")
# print(sowtazhang(item, None, None))
#
#
# item = MyObject("https://sowtazhang.ir/product/saramonic-lavmicro-u1b/")
# print(sowtazhang(item, None, None))
