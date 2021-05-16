import re

import requests
from bs4 import BeautifulSoup


def yamahairan(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    p = soup.find("span", attrs={"class": "amount"})
    a = re.sub(r',', '', p.text).strip()
    b = re.split(r'\s', a)
    if b[0] == '۰':
        return -1
    else:
        return int(b[0])
