import re

import requests
from bs4 import BeautifulSoup


def janebi(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("div", attrs={"class": "add-to-basket ripple-btn has-ripple add_to_basket"}):
        p = soup.find("span", attrs={"id": "ProductPrice"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
