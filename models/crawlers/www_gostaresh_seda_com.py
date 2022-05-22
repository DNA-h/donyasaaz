import re
import logging
import sys
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import math


def gostaresh(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        sys.path.append("C:\\Users\\zgb\\Desktop\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\zgb\\Desktop\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    disabled = soup.find("span", attrs={"class": "btn disabled btn-green"})
    if disabled and 'disabled' not in disabled.attrs:
        return -1
    div = soup.find("a", attrs={"class": re.compile("add-to-cart btn*")})
    if div is None:
        return -1
    div = div.parent if div is not None else disabled.parent
    p = div.find("div", attrs={"class": "pe"})
    if p is None:
        return -1
    s = p.find("b")
    a = re.sub(r',', '', s.text).strip()
    b = re.findall(r'\d+', a)
    if len(b) ==0:
        return -1
    return math.floor(int(b[0]) / 10)
