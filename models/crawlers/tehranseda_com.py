import re

import requests
from bs4 import BeautifulSoup


def tehranseda(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    s = soup.find("button", attrs={"id": "button-cart"})
    if s is not None:
        p = soup.find("span", attrs={"class": "number", "itemprop": "price"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
