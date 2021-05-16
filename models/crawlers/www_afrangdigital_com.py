import re

import requests
from bs4 import BeautifulSoup


def afrangdigital(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button", attrs={"class": "button pro-add-to-cart"}):
        p = soup.find("p", attrs={"class": "special-price"})
        s = p.find("price")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
