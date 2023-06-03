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


def sotplus(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        sys.path.append("C:\\Users\\USER\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\USER\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        try:
            element = driver.find_element(By.CSS_SELECTOR, '.is_stuck')
            first_strong = element.find_element(By.CSS_SELECTOR, ".woocommerce-Price-currencySymbol")
            parent_element = first_strong.find_element(By.XPATH, "..")

            # Get the HTML content of the parent element
            html_content = parent_element.get_attribute('innerHTML')

            # Extract the pure text using regular expressions
            price_text = re.sub('<[^>]+>', '', html_content)

            if price_text != "":
                price_text = int(price_text)
                driver.close()
                return price_text
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