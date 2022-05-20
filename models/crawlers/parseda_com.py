import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def parseda(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "btn btn-primary"}):
        soup.find("span", attrs={"style": "display:none;padding:5px"})
        return -1
    if soup.find("span", attrs={"content": "1"}):
        return -1
    if soup.find("button", attrs={"class": "btn btn-primary add-to-cart"}):
        div = soup.find("div", attrs={"class": "current-price"})
        if div is None:
            return -1
        p = div.find("span", attrs={"itemprop":"price"})
        if p is None:
            return -1
        if p is 1:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
