import re

import requests
from bs4 import BeautifulSoup


def esam(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("span", attrs={"id": "ctl00_ctl00_main_main_LBLpriceIfDiscount"})
    if p.text != '':
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
    else:
        s = soup.find("span", attrs={"id": "ctl00_ctl00_main_main_LBLprice"})
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
    return int(b[0])  # todo where is None
