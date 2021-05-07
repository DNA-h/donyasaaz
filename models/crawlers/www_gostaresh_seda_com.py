import re

import requests
from bs4 import BeautifulSoup


def gostaresh(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
        return None

    if soup.find("span", attrs={"class": "btn disabled btn-green"}):
        return -1
    else:
        p = soup.find("div", attrs={"class": "pe", "style": "font-size:14px"})
        s = p.find("b")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0]) / 10
