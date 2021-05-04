import re

import requests
from bs4 import BeautifulSoup


def max_shop(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("span", attrs={"id": "buy"}):
        p = soup.find("div", attrs={"class": "price"})
        s = p.find("div")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
