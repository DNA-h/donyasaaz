import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def esam(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("input" , attrs = {"class" : "btn btn-primary btn-buy SpaceMargin addToBasket"}):
        p =soup.find("span" , attrs = {"id" : "ctl00_ctl00_main_main_LBLpriceIfDiscount"})
        if p is not None:
            a = re.sub(r',', '', p.text).strip()
            b = re.findall(r'\d+', a)
            if len(b) > 0:
                return int(b[0])
        p = soup.find("span" , attrs = {"id" : "ctl00_ctl00_main_main_LBLprice"})
        if p is not None:
            a = re.sub(r',', '', p.text).strip()
            b = re.findall(r'\d+', a)
            if len(b) > 0:
                return int(b[0])
    return -1
