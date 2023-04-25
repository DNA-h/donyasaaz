import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def iranloop(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    notavail = soup.find("div", attrs={"class": "product-availability"})
    if notavail is None:
        s = soup.find("span", attrs={"class": "price"})
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        if len(b) == 0 :
            return -1
        return int(b[0])
    else:
        return -1
