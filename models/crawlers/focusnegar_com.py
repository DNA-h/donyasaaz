import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def focusnegar(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("input", attrs={"class": "ProductDetailButton ProductDetailButtonAddBasket"}):
        div = soup.find("div", attrs={"class": "RowMarginTen ItemPriceDetail"})
        if div is None:
            return -1
        a = re.sub(r',', '', div.text).strip()
        b = re.findall(r'\d+', a)
        if len(b) == 0:
            return -1
        return int(b[0])
    else:
        return -1
