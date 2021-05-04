import re

import requests
from bs4 import BeautifulSoup


def digikala(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("div", attrs={"class": "c-product__seller-row c-product__seller-row--add-to-cart"}):
        p = soup.find("div", attrs={"class": "c-product__seller-price-real"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
