import re

import requests
from bs4 import BeautifulSoup


def tehrandj(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("a", attrs={"class": "add-to-cart"}):
        p = soup.find_all("div", attrs={"class": "special-price"})
        if len(p) == 0:
            p = soup.find_all("div", attrs={"class": "normal-price"})
            if len(p) == 0:
                return -1
        if len(p) == 1:
            s = p[0].find("span", attrs={"class": "price"})
        else:
            s = p[1].find("span", attrs={"class": "price"})
        if s is None:
            return -1
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
