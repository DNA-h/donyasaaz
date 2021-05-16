import re

import requests
from bs4 import BeautifulSoup


def edbazar(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    p = soup.find("ul", attrs={"ng-hide": "Good.Tender"})
    if p is not None:
        s = p.select("li span")
        ss = re.sub(r'\s+', ' ', s[0].text).strip()
        a = re.sub(r',', '', ss).strip()
        b = re.findall(r'\d+', a)
        if a == 'تماس بگیرید':
            return -1
        return int(b[0])
    else:
        return -1
