import re

import requests
from bs4 import BeautifulSoup


def pakhsh(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("div", attrs={"class": "price-wrapper"})
    if p is not None:
        s = p.find("ins")
        if s is None:
            a = re.sub(r',', '', p.text).strip()
            b = re.split(r'\s', a)
        else:
            a = re.sub(r',', '', s.text).strip()
            b = re.split(r'\s', a)
        return int(b[0])
    else:
        return -1
