import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def divar(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    p = soup.find_all("p", string="قیمت")
    if len(p) ==0:
        return -1
    a = re.sub(r'٫', '', p[0].parent.parent.text).strip()
    b = re.findall(r'\d+', a)
    return int(b[0])
