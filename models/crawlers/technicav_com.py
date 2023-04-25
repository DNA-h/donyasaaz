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

def technicav(link, headers, site):
    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
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

    if soup.find("div",attrs={"class": "row skel-pro-single loaded"}):
        details = soup.find("div", attrs={"class": "row skel-pro-single loaded"})
        if details.find("div", attrs={"class": "product-price"}):
            if details.find("div",attrs={"class": "old-price"}):
                div = details.find("div",attrs={"class": "new-price"})
                span = div.find_all("span")[0]
                a = re.sub(r',', '', span.text).strip()
                b = re.findall(r'\d+', a)
                return int(b[0])  
            else:
                return -1 
        else:
            return -1
    else:
        return -1
