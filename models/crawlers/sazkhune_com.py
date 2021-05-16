import re

import requests
from bs4 import BeautifulSoup


def sazkhune(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("a", attrs={"class": "btn btn-product btn-custom btn-lg add_to_basket"}):
        p = soup.find("span", attrs={"id": "ProductPrice"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
