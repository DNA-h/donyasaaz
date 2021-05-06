import re

import requests
from bs4 import BeautifulSoup


def emalls(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("h3", attrs={"class": "itemprice mb10"})
    if p is not None:
        s = re.sub(r'٫', '', p.text).strip()
        a = re.sub(r'\s+', ' ', s).replace(",","")
        b = re.findall(r'\d+', a)
        if a == "ناموجود" or a == "بدون قیمت":
            return -1
        else:
            return int(b[0])
    return -1
