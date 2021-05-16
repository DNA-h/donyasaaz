import re
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def musicala(link, headers, site):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), options=chrome_options)
        driver.get(link.url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "exclusive btn btn-warning"}):
        out_of_stock = soup.find("span", attrs={"id":"availability_value"})
        if out_of_stock is not None and out_of_stock.text =='این مدل تمام شده است ':
            return -1
        div = soup.find("p", attrs={"class": "our_price_display"})
        if div is None:
            return -1
        p = div.find("span", attrs={"id":"our_price_display"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
