import re

import requests
from bs4 import BeautifulSoup


def asarayan(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "our_price_display"})
    if p is not None:
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        if re.findall(r'^\D+', p.text)[0] == "ناموجود":
            return -1
        else:
            return int(b[0])
