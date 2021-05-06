import re

import requests
from bs4 import BeautifulSoup


def egerd(link, headers, site):
    try:
        s= requests.Session()
        response = s.get(link, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    s= soup.find("button", attrs={"class": "btn btn-secondary"})
    if s is not None:
        p = soup.find("div",attrs={"class":"d-flex justify-content-end align-items-center"})
        a = re.sub(r',', '', p.find("p").text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
