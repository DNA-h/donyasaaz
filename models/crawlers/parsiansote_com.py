import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def parsiansote(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button", attrs={"name": "add-to-cart"}):
        return -1
    else:
        p = soup.find("span", attrs={"class": "price"})
        if p.find("span", attrs={"class": "matrix_wolffinal-price"}):
            s = p.find("span", attrs={"class": "matrix_wolffinal-price"})
        else:
            s = p.find("bdi")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
