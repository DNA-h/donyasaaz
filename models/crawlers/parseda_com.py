import re

import requests
from bs4 import BeautifulSoup


def parseda(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"class": "btn btn-primary add-to-cart"}):
        div = soup.find("div", attrs={"class": "current-price"})
        if div is None:
            return -1
        p = div.find("span", attrs={"itemprop":"price"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
