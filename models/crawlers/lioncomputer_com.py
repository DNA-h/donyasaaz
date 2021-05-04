import re

import requests
from bs4 import BeautifulSoup


def lioncomputer(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("div", attrs={"id": "product-price"})
    if p is not None:
        s = p.find("strong")
        if s is not None:
            ss = re.sub(r'\s+', ' ', s.text).strip()
            a = re.sub(r',', '', ss)
            b = re.findall(r'\d+', a)
            if a == "ناموجود":
                return -1
            else:
                return int(b[0])
    else:
        return -1
