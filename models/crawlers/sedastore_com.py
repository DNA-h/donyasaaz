import re

import requests
from bs4 import BeautifulSoup


def sedastore(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "price"})
    if soup.find("p", attrs={"class": "woocommerce-error"}) or soup.find("p",
                                                                         attrs={"class": "price"}).find("strong"):
        return -1
    else:  # todo "موجود شد به من اطلاع بده"
        # https://sedastore.com/product/%d9%87%d8%af%d9%81%d9%88%d9%86-hd-280-pro-%d8%b3%d9%86%d9%87%d8%a7%db%8c%d8%b2%d8%b1/
        s = p.find("ins")
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
        else:
            a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
