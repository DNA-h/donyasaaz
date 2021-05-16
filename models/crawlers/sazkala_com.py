import re

import requests
from bs4 import BeautifulSoup


def sazkala(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    p = soup.find("p", attrs={"class": "price"})
    if soup.find("div", attrs={"class": "absolute-label-product outofstock-product"}):
        return -1
    else:
        s = p.find("ins")
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
        else:
            a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
