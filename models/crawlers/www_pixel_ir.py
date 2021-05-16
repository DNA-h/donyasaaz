import re

import requests
from bs4 import BeautifulSoup


def pixel(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button",
                 attrs={"class": "btn btn-default btn-large add-to-cart btn-full-width btn-spin"}):
        p = soup.find("div", attrs={"class": "current-price"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        if a == "تماس بگیرید":
            return -1
        else:
            return int(b[0])
    else:
        return -1
