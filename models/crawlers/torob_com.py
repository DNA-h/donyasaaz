import re
import logging
import sys
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def torob(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('log-level=3')
        sys.path.append(os.path.abspath("chromedriver_95.exe"))
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver_95.exe"), options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    p = soup.find("h2", attrs={"class": "jsx-1813026706"})
    if p is not None:
        s = re.sub(r'٫', '', p.text).strip()
        a = re.sub(r'\s+', ' ', s)
        b = re.findall(r'\d+', a)
        if a == "ناموجود" or a == "بدون قیمت":
            return -1
        else:
            return int(b[0])
