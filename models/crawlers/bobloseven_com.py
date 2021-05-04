import re

import requests
from bs4 import BeautifulSoup


def bobloseven(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("span", attrs={"class": "price"})
    if p is not None:
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
    if soup.find("div", attrs={"class": "status"}):
        s = soup.find("div", attrs={"class": "status"})
        a = re.sub(r'\s+', '', s.text)
    if a == "ناموجود" or a == "بهزودی":  # todo possible bug
        return -1
    else:
        return int(b[0])  # todo possible bug
