import re

import requests
from bs4 import BeautifulSoup


def iranloop(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    p = soup.find("p", attrs={"class": "our_price_display"})
    if soup.find("p", attrs={"id": "availability_statut"}).text == " موجود است" or \
            soup.find("span", attrs={"id": "availability_value"}).text == "موجود است":
        s = p.find("span", attrs={"class": "price"})
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        else:  # todo DNA added this
            return -1
    else:  # todo https://iranloop.ir/%DA%A9%D8%A7%D8%B1%D8%AA-%D8%B5%D8%AF%D8%A7-universal-audio-apollo-solo-usb3
        return -1
