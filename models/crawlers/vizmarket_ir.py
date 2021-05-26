import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def vizmarket(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button", attrs={"class": "add-card"}) :
        p = soup.find("div", attrs={"class", "unit fi fi-unit"})
        if p is None:
            return -1
        a = re.sub(r',', '', p.parent.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    return -1
