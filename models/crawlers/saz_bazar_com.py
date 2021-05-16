import re

import requests
from bs4 import BeautifulSoup


def saz_bazar(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.find("div", attrs={"class": "current-price"})
    if p is not None:
        s = p.find("span", attrs={"itemprop": "price"})
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        if a == 'تماس بگیرید':
            return -1
        else:
            return int(b[0])
    else:
        return -1
