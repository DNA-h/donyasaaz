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

def falude(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-gpu")
        sys.path.append("C:\\Users\\zgb\\Desktop\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\zgb\\Desktop\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button dk-button"}):
        div = soup.find(attrs={"class": "price"})
        if div is None:
            return -1
        p = div.find_all(attrs={"class":"woocommerce-Price-amount amount"})
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
