import re

import requests
from bs4 import BeautifulSoup


def logilook(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    p = soup.find("span", attrs={"itemprop": "price"})
    if p is not None:
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        if a == "اتمام موجودی":
            return -1
        else:
            return int(b[0])
    else:
        return -1
