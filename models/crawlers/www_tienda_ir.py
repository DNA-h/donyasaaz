import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def tienda(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.find("ins", attrs={"class": "font-size-36 text-decoration-none"})
    if p is None:
        return -1
    a = re.sub(r',', '', p.text).strip()
    b = re.findall(r'\d+', a)
    if int(b[0]) == 0:
        return -1
    else:
        return int(b[0]) * 1000
