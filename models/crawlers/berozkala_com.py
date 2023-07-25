import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys

def berozkala(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    while(True):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        div = soup.find("span", attrs={"class": "price"})
        img = div.find("img")
        if img is None:
            break
        else:
            time.sleep(1)
    driver.close()

    if soup.find("button", attrs={"class": "single_add_to_cart_button button"}):
        div = soup.find("p", attrs={"class": "price"})
        if div is None:
            return -1
        p = div.find_all("span", attrs={"id":"_showPriceInHomePage"})
        if len(p) == 0:
            return -1
        elif len(p) == 1:
            a = re.sub(r',', '', p[0].text).strip()
        else:
            a = re.sub(r',', '', p[1].text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
