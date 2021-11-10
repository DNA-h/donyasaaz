import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def sazzbazz(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button", attrs={"class": re.compile("single_add_to_cart_button button alt*")}):
        div = soup.find("div", attrs={"class": "summary-inner"})
        p = div.find("p", attrs={"class": "price"}).find_all("span", attrs={"class": "woocommerce-Price-amount amount"})
        if p is None or len(p) == 0:
            return -1
        elif len(p) == 1:
            a = re.sub(r',', '', p[0].text).strip()
        elif p[0].sourceline == p[1].sourceline:
            a = re.sub(r',', '', p[1].text).strip()
        else:
            a = re.sub(r',', '', p[0].text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
