import re

import requests
from bs4 import BeautifulSoup


def ava_avl(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
        p = soup.findAll("span", attrs={"class": "woocommerce-Price-amount amount"})
        for i in range(0, len(p)):
            if ("class" in p[i].parent.attrs and ("cart-contents" in p[i].parent.attrs["class"])) or \
                    ("class" in p[i].parent.parent.attrs and "price-total-w" in p[i].parent.parent.attrs["class"]):
                continue
            elif p[i].parent.name == "del":
                continue
            else:
                a = re.sub(r',', '', p[i].text).strip()
                b = re.findall(r'\d+', a)
                return int(b[0])
        return -1
    else:
        return -1
