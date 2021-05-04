import re

import requests
from bs4 import BeautifulSoup


def chavoosh110(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if p is not None:
        s = p.find("ins")
        if s is None:
            s = p.find("bdi")
        if s is not None:  # todo possible bug
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            if a == 'تماس بگیرید':
                return -1
        return int(b[0])
    else:
        return -1
