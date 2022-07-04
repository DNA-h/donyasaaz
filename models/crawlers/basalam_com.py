import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sys


def basalam(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-gpu")
        sys.path.append("C:\\Users\\USER\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\USER\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "add-to-cart__button bs-button bs-button--lg bs-button-fill bs-button-fill--primary bs-button--full-width"}):
        div = soup.find("span", attrs={"class": "add-to-cart__content-price"})
        if len(div) == 0:
            return -2
        elif len(div) == 1:
            a = re.sub(r',', '', div.text).strip()
        else:
            a = re.sub(r',', '', div.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -3
