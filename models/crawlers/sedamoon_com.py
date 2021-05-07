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

    if soup.find("div", attrs={"class": "sticky-add-to-cart"}):
        p = soup.find("p", attrs={"class": "price"})
        s = p.find("ins")
        if s != None:
            a = re.sub(r',', '', s.text).strip()
        else:
            a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
