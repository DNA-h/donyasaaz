import re

import requests
from bs4 import BeautifulSoup


def bia2piano(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"name": "add-to-cart"}):
        p = soup.find("p", attrs={"class": "price"})
        if p.find("ins") is not None:
            s = p.find("ins")
        else:
            s = p.find("bdi")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:  # todo "0 تومان" https://bia2piano.ir/product/microphone-studio-audio-technica-at2031/
        return -1
