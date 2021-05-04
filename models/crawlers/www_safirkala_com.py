import re

import requests
from bs4 import BeautifulSoup


def safirkala(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if p is not None:
        if p.find("ins"):
            p = soup.find("p", attrs={"class": "price"}).find("ins")
            s = re.sub(r'\s+', ' ', p.text).strip()
            a = re.sub(r',', '', s).strip()
            b = re.split(r'\s', a)
            return b[1]  # todo return int(b[0])
        else:
            s = re.sub(r'\s+', ' ', p.text).strip()
            a = re.sub(r',', '', s).strip()
            b = re.split(r'\s', a)
        return int(b[0])
    else:
        return -1
