import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def beyerdynamic(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.findAll("span", attrs={"class": "woocommerce-Price-amount amount"})
    if len(p) == 0:
        p = soup.findAll("span", attrs={"class": "price"})
    if len(p) != 0:
        if len(p) > 1:
            s = p[1]
        else:
            s = p[0]
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        return -1
    else:
        return -1
