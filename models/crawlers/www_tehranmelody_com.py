import re

import requests
from bs4 import BeautifulSoup


def tehranmelody(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"id": "button-cart"}):
        p = soup.find("div", attrs={"class": "price"})
        s = re.sub(r'\s+', ' ', p.text).strip()
        a = re.sub(r',', '', s)
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
