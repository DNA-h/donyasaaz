import re

import requests
from bs4 import BeautifulSoup


def janebi(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("div", attrs={"class": "add-to-basket ripple-btn has-ripple add_to_basket"}):
        p = soup.find("span", attrs={"id": "ProductPrice"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
