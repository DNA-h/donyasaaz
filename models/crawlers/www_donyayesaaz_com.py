import re

import requests
from bs4 import BeautifulSoup


def donyayesaaz(link, headers):
    try:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print("donyayesaaz")
        print(e)
        return None

    p = soup.find("span", attrs={"id": "final-price"})
    if p is not None:
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0]) / 10
    else:
        return -1
