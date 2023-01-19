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

def divar(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument("--headless")
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

    p = soup.find_all("p", string="قیمت")
    if len(p) == 0:
        return -1
    a = re.sub(r'٬', '', p[0].parent.parent.text).strip()
    b = re.findall(r'\d+', a)
    return int(b[0])
