import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def emalls(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')
        driver = webdriver.Chrome(executable_path="C:\\Users\\Administrator\\Desktop\\donyasaaz\\chromedriver.exe", options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    p = soup.find("h3", attrs={"class": "itemprice mb10"})
    if p is not None:
        s = re.sub(r'٫', '', p.text).strip()
        a = re.sub(r'\s+', ' ', s).replace(",","")
        b = re.findall(r'\d+', a)
        if a == "ناموجود" or a == "بدون قیمت":
            return -1
        else:
            return int(b[0])
    return -1
