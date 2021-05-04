import re

import requests
from bs4 import BeautifulSoup


def zanbil(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("div", attrs={"id": "product-price"})
    if p is not None:
        s = p.find("span", attrs={"itemprop": "price"})
        if s is not None:
            ss = re.sub(r'\s+', '', s.text).strip()
            a = re.sub(r',', '', ss)
            b = re.findall(r'\d+', a)
            return int(b[0])
        else:
            return -1
