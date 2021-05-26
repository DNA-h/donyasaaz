import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def npdigi_com(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button alt wc-variation-selection-needed add_to_card_ajax_avis"}):
        div = soup.find("span", attrs={"class": "price"})
        if div is None:
            return -1
        p = div.find("span")
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        import math
        return math.floor(int(b[0])/10)
    else:
        return -1
