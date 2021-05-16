import re

import requests
from bs4 import BeautifulSoup


def iranfender(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button", attrs={"class": "btn btn-primary btn-lg btn-block"}):
        div = soup.find("div", attrs={"class": "col-md-12 pull-right price-box"})
        if div is None:
            return -1
        p = div.find("h2")
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
