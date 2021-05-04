import re

import requests
from bs4 import BeautifulSoup


def bokehland(link, headers, site):
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
        s = p.find("span")
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.split(r'\s', a)
            return int(b[0])
        else:  # todo possible bug
            return -1
