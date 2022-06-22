import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def khaneyesaaz(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "uk-button uk-button-primary addtocart-button uk-width-1-1 addtocart-button"}):
        div = soup.find("span", attrs={"class": "PricesalesPrice"})
        if div is None:
            siv = soup.find("span", attrs={"class": "PricediscountedPriceWithoutTax"})
            a = re.sub(r',', '', siv.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        else:
            a = re.sub(r',', '', div.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])

    else:
        return -1
