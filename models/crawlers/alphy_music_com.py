import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def alphy_music(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    p = soup.find("span", attrs={"id": "hikashop_product_price_main"})
    if p is None:
        return -1
    s = p.find("span", attrs={"span","hikashop_product_price hikashop_product_price_0"})
    if s is None:
        return -1
    a = re.sub(r',', '', s.text).strip()
    b = re.findall(r'\d+', a)
    return int(b[0])
