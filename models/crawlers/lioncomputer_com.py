import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def lioncomputer(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.find("div", attrs={"id": "product-price"})
    if p is not None:
        s = p.find("strong")
        if s is not None:
            ss = re.sub(r'\s+', ' ', s.text).strip()
            a = re.sub(r',', '', ss)
            b = re.findall(r'\d+', a)
            if a == "ناموجود":
                return -1
            else:
                return int(b[0])
    else:
        return -1
