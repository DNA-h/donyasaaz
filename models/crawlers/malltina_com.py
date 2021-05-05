import re

import requests
from bs4 import BeautifulSoup


def malltina(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"class": "btn-addToCart"}):
        p = soup.find("div", attrs={"class": "final-price"})
        s = p.find("strong")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:  # todo "0 تومان" https://malltina.com/product/mlt-76231
        return -1
