import re

import requests
from bs4 import BeautifulSoup


def digiseda(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("div", attrs={"id": "our_price_display", "class": "prd-price"})
    if p is not None:  # TODO check else for this if
        if soup.find("span", attrs={"id": "our_price_display", "class": "price"}) is None:
            s = re.sub(r'\s+', ' ', p.text).strip()
            a = re.sub(r',', '', s)
            b = re.findall(r'\d+', a)
            return int(b[0])
        else:
            return -1
    if soup.find("div", attrs={"class": "subpriceform"}):
        return -1
