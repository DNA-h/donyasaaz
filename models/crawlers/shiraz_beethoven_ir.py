import re

import requests
from bs4 import BeautifulSoup


def shiraz_beethoven(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button", attrs={"class": "btn btn-fill-out btn-addtocart js-loginplease"}):
        div = soup.find("div", attrs={"class": "product_description"})
        if div is None:
            return -1
        p = div.find("span", attrs={"class":"price"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
