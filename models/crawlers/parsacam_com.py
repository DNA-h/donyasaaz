import re

import requests
from bs4 import BeautifulSoup


def parsacam(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
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