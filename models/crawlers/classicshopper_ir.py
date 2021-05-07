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

    if soup.find("a" , attrs = {"class" : "add-to-cart"}):
        p = soup.find("div", attrs={"class": "item-newprice"})
        s = re.sub(r'\s+', ' ', p.text).strip()
        a = re.sub(r',', '', s)
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
