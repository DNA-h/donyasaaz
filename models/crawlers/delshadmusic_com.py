import re

import requests
from bs4 import BeautifulSoup


def delshadmusic(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button", attrs={"name": "add-to-cart"}):
        p = soup.find("span", attrs={"class": "woocommerce-Price-amount amount"})
        s = re.sub(r'\s+', ' ', p.text).strip()
        a = re.sub(r',', '', s)
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
