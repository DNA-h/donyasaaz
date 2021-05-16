import re

import requests
from bs4 import BeautifulSoup


def ertebat(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("span", attrs={"itemprop": "price"}):
        p = soup.find("span", attrs={"itemprop": "price"})
        s = re.sub(r'\s+', ' ', p.text).strip()
        a = re.sub(r'\.', '', s)
        b = re.findall(r'\d+', a)
        return int(b[0]) / 10
    else:
        return -1
