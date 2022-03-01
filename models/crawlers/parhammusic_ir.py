import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def parhammusic(link, headers, site):
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

    p = soup.find("div", attrs={"class": "gheimat_kala"})
    if p is None:
        return -1
    a = re.sub(r',', '', p.text).strip()
    b = re.findall(r'\d+', a)
    return int(b[0])
