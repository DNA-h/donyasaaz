import re

import requests
from bs4 import BeautifulSoup


def sedamoon(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if p:  # todo "0 تومان"
        # https://sedamoon.com/product/%d9%87%d8%af%d9%81%d9%88%d9%86-%d8%b3%d9%86%d9%87%d8%a7%db%8c%d8%b2%d8%b1-%d9%85%d8%af%d9%84-sennheiser-hd280-pro/?utm_medium=PPC&utm_source=Torob
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
