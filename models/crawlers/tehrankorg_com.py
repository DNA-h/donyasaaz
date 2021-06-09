import re
import logging
import math
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def tehrankorg(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    p = soup.find("a", attrs={"class": re.compile("edd-add-to-cart button")})
    if p is not None:
        if 'data-price' not in p.attrs:
            return -1
        return math.floor(int(p.attrs['data-price']) / 10)
    return -1
