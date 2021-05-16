import re

import requests
from bs4 import BeautifulSoup


def gilsara(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.find("p", attrs={"class": "price"})
    if p is not None:
        if soup.find("p", attrs={"class": "stock out-of-stock"}) is None:
            s = p.find("ins")
            if s is None:
                s = p.find("bdi")
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        else:
            return -1
