import re

import requests
from bs4 import BeautifulSoup


def malltina(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button", attrs={"class": "btn-addToCart"}):
        p = soup.find("div", attrs={"class": "final-price"})
        s = p.find("strong")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        if int(b[0]) == 0:
            return -1
        else:
            return int(b[0])
    else:
        return -1
