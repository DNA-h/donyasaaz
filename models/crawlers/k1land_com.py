import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def k1land(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="C:\\Users\\Administrator\\Desktop\\donyasaaz\\chromedriver_95.exe", options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    s= soup.find("span", attrs={"itemprop": "price"})
    if s is not None:
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        if len(b) == 0:
            return -1
        return int(b[0])
    else:
        return -1
