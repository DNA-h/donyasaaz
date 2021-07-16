import re
import logging
import math
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def afrangdigital(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button", attrs={"class": "button pro-add-to-cart"}):
        p = soup.find("p", attrs={"class": "special-price"})
        s = p.find("price")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return math.floor(int(b[0])/10)
    else:
        return -1
