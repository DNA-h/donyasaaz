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

def mobit(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        sys.path.append("C:\Users\USER\donyasaaz\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\Users\USER\donyasaaz\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class":"mt-6 d-block w-100 v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--large app-button lg-button white--text"}):
        p = soup.find("div", attrs={"class": "product-summery v-card v-sheet v-sheet--outlined theme--light"})
        if p is None:
            return -1
        s = p.find("div",attrs={"class":"currency font-s-12 text-high--text"})
        if s is None:
            return -1
        a = re.sub(r',', '', s.parent.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    return -1
