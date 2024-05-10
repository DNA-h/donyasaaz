import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import math
import sys

def yamahairan(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
         
        chrome_options.add_argument('--disable-dev-shm-usage')
        sys.path.append("C:\\Users\\hamed\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\hamed\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.set_page_load_timeout(40);driver.get(link.url);
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("span", attrs={"class": "lnkShowMsg add-to-cart col-xs-12"}):
        p = soup.find("span", attrs={"class": "amount"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        if b[0] == '۰':
            return -1
        else:
            return math.floor(int(b[0]) /10)
    return -1
