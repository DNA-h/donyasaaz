import re

import requests
from bs4 import BeautifulSoup


def kalaoma(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button",
                 attrs={"class": "km-btn km-theme-2 width-100 km-add-product-to-cart KM_addProductToCart"}):
        p = soup.find("span", attrs={"itemprop": "price"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
