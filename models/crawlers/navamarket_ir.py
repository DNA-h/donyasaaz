import re

import requests
from bs4 import BeautifulSoup


def navamarket(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.find("span", attrs={"class": "price", "itemprop": "price"})
    if p.attrs['content'] == '1' or p.attrs['content'] == '4':
        return -1
    else:
        s = re.sub(r'\s+', ' ', p.text).strip()
        a = re.sub(r',', '', s)
        b = re.findall(r'\d+', a)
        return int(b[0])
