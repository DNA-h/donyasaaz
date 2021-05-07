import re

import requests
from bs4 import BeautifulSoup


def seda_center(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("a", attrs={"class": "hikabtn hikacart"}):
        p = soup.find("span", attrs={"class": "hikashop_product_price hikashop_product_price_0"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
