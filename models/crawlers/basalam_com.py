import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def basalam(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "add-to-cart__button bs-button bs-button--lg bs-button-fill bs-button-fill--primary bs-button--full-width"}):
        div = soup.find("span", attrs={"class": "add-to-cart__content-price"})
        if len(div) == 0:
            return -2
        elif len(div) == 1:
            a = re.sub(r',', '', div.text).strip()
        else:
            a = re.sub(r',', '', div.text).strip()
        b = re.findall(r'\d+', a)
        return div
    else:
        return -3
