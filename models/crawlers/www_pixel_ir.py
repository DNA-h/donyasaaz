import re
import logging
import requests
from urllib3.exceptions import InsecureRequestWarning
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def pixel(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), options=chrome_options)
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("span", attrs={"class":"sms-alert-label"}):
        return -1

    if soup.find("button",
                 attrs={"class": "btn btn-default btn-large add-to-cart btn-full-width btn-spin"}):
        p = soup.find("div", attrs={"class": "current-price"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        if a == "تماس بگیرید":
            return -1
        else:
            return int(b[0])
    else:
        return -1
