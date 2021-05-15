import re

import requests
from bs4 import BeautifulSoup


def barbadpiano(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
        div = soup.find("p", attrs={"class": "price"})
        if div is None:
            return -1
        p = div.find_all("span", attrs={"class": "woocommerce-Price-amount amount"})
        if len(p) == 0:
            return -1
        elif len(p) == 1:
            a1 = re.sub(r',', '', p[0].text).strip()
            b1 = re.findall(r'\d+', a1)
            return int(b1[0])
        else:
            a1 = re.sub(r',', '', p[0].text).strip()
            a2 = re.sub(r',', '', p[1].text).strip()
            b1 = re.findall(r'\d+', a1)
            b2 = re.findall(r'\d+', a2)
            return min(int(b1[0]), int(b2[0]))
    else:
        return -1
