import re

import requests
from bs4 import BeautifulSoup


def ghesticlub(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("div", attrs={"class": "defme"})
    if soup.find("input", attrs={"name": "sabad"}):
        s = re.sub(r'\s+', ' ', p.text).strip()
        a = re.sub(r',', '', s).strip()
        b = re.split(r'\s', a)
        if len(b) == 4:
            b[0] = b[2]
            return int(b[0])
        elif b[0] == "تومان":
            return -1
    else:
        return -1
