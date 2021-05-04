import re

import requests
from bs4 import BeautifulSoup


def echokowsar(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("button", attrs={"class": "btn btn-primary flex-grow-1 flex-md-grow-0"}):
        p = soup.find("h5", attrs={"itemprop": "offers"})
        s = p.find("span")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
