import re

import requests
from bs4 import BeautifulSoup


def yamahairan(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("span", attrs={"class": "amount"})
    a = re.sub(r',', '', p.text).strip()
    b = re.split(r'\s', a)
    if b[0] == '۰':
        return -1
    else:
        return int(b[0])
