import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def head_phone(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None
    if soup.find("a",attrs={"class":"btn btn-cart addToCart"}):
        div = soup.find("div", attrs={"class":"price-box text-right"})
        if div is None:
            return -1
        p = div.find("span", attrs={"class": "price"})
        if p:
            a = re.sub(r',', '', p.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
    return -1
