import re

import requests
from bs4 import BeautifulSoup


def noornegar(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
        p = soup.find("p", attrs={"class": "price"})
        if p.find("ins") is not None:
            s = p.find("ins")
        else:
            s = p.find("bdi")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
