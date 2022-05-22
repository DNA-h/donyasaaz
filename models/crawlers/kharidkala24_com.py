import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def kharidkala24(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("span", attrs={"class": "dk-button-container hasIcon"}):
        div = soup.find(attrs={"class": "price"})
        if div is None:
            return -1
        p = div.find_all("span", attrs={"class":"woocommerce-Price-amount amount"})
        if len(p) == 0:
            return -1
        elif len(p) == 1:
            a = re.sub(r'\.', '', p[0].text).strip()
        else:
            a = re.sub(r'\.', '', p[1].text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
