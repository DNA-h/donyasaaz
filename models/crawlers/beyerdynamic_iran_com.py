import re

import requests
from bs4 import BeautifulSoup


def beyerdynamic(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.findAll("span", attrs={"class": "woocommerce-Price-amount amount"})
    if len(p) == 0:
        p = soup.findAll("span", attrs={"class": "price"})
    if len(p) != 0:
        if len(p) > 1:
            s = p[1]
        else:
            s = p[0]
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        return -1
    else:
        return -1
