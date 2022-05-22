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
import sys

def sazhouse(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-features=NetworkService")  ##this did it for me
        # chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        sys.path.append("C:\\Users\\zgb\\Desktop\\donyasaaz\\chromedriver.exe")
        driver = webdriver.Chrome(executable_path="C:\\Users\\zgb\\Desktop\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        driver.get(link.url)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "totlaPrice")))
    except:
        return -1
    soup = BeautifulSoup(driver.page_source, "html.parser")
    if soup.find("span", attrs={"class": "addBasketText"}):
        p = soup.find(attrs={"id": "totlaPrice"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
