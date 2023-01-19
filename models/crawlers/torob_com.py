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
        print('start');
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--log-level=3')
        print(0)
        sys.path.append("C:\\Users\\USER\\donyasaaz\\chromedriver.exe")
        print('append')
        driver = webdriver.Chrome(executable_path="C:\\Users\\USER\\donyasaaz\\chromedriver.exe",
                                  options=chrome_options)
        print(1)
        driver.get(link.url)
        print(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    print(3)
    p = soup.find("div", attrs={"class": "jsx-e248faa755581a69 price"})
    if p is not None:
        s = re.sub(r'٫', '', p.text).strip()
        a = re.sub(r'\s+', ' ', s)
        b = re.findall(r'\d+', a)
        if a == "ناموجود" or a == "بدون قیمت":
            return -1
        else:
            return int(b[0])
