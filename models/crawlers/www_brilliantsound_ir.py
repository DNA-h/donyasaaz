import re

import requests
from bs4 import BeautifulSoup


def brilliantsound(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"class": "btn btn-cta btn-flash ripple"}):
        div = soup.find("div", attrs={"class": "product-single-price"})
        p = div.find_all("span", attrs={"class":"woocommerce-Price-amount amount"})
        if len(p) == 1:
            a = re.sub(r',', '', p[0].text).strip()
        else:
            a = re.sub(r',', '', p[1].text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
