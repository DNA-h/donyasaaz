import re

import requests
from bs4 import BeautifulSoup


def hajigame(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if p is None or p.text == "":
        return -1
    else:
        if p.find("ins"):
            s = p.find("ins")
            a = re.sub(r',', '', s.text).strip()
        else:
            a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        if a == "تماس بگیرید":
            return -1
        else:
            return int(b[0])
