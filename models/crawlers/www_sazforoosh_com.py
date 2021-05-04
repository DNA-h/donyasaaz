import re

import requests
from bs4 import BeautifulSoup


def sazforoosh(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("div", attrs={"class": "price"})
    if soup.find("div", attrs={"id": "product"}).find('p'):
        return -1
    else:
        s = p.find("h3")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
