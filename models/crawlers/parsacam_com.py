import re

import requests
from bs4 import BeautifulSoup


def parsacam(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("div", attrs={"class": "add-to-cart-wrapper"}):
        p = soup.find("span", attrs={"class": "price"})
        if p.find("span"):
            s = p.find("ins")
        else:
            s = p
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1