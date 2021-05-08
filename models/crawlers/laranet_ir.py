import re

import requests
from bs4 import BeautifulSoup


def laranet(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("a", attrs={"class": "add-to-shoppingcart"}):
        div = soup.find("div", attrs={"class": "ProductShowPrice"})
        if div is None:
            return -1
        p = div.find("span")
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
