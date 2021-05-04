import re

import requests
from bs4 import BeautifulSoup


def torob(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("h2", attrs={"class": "jsx-1813026706"})
    if p is not None:
        s = re.sub(r'٫', '', p.text).strip()
        a = re.sub(r'\s+', ' ', s)
        b = re.findall(r'\d+', a)
        if a == "ناموجود" or a == "بدون قیمت":
            return -1
        else:
            return int(b[0])
