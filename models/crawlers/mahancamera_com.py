import re

import requests
from bs4 import BeautifulSoup


def mahancamera(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if p is not None:
        s = p.find("strong")
        if s is not None:  # todo possible bug
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            if a == 'برای قیمت تماس بگیرید':
                return -1
            else:
                return int(b[0])
    else:
        return -1
