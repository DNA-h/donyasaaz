import re

import requests
from bs4 import BeautifulSoup


def diddovom(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if p is not None:
        s = p.find("ins")
        if s is None:
            s = p.find("bdi")
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        else:
            return -1
    else:
        return -1
