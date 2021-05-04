import re

import requests
from bs4 import BeautifulSoup


def classicshopper(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("div", attrs={"class": "item-newprice"})
    if p is not None:
        s = p.find("span")
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
        if a == "تومان":  # todo possible bug
            return -1
        else:  # todo possible bug
            return int(b[0])
    else:
        return -1
