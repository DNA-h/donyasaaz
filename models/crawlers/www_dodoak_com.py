import re

import requests
from bs4 import BeautifulSoup


def dodoak(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("div", attrs={"class":"content_prices clearfix hidden"}):
        return -1
    s = soup.find("p", attrs={"class": "our_price_display"})
    if s is None:
        s = soup.find("span", attrs={"class": "our_price_display"})
    if s is not None:
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
