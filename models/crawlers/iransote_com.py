import re

import requests
from bs4 import BeautifulSoup


def iransote(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if soup.find("p", attrs={"class": "stock out-of-stock"}) is None:
        s = p.find("ins")
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
        else:
            a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
