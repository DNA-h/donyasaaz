import re

import requests
from bs4 import BeautifulSoup


def head_phone(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("span", attrs={"class": "price"})
    if p:
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
