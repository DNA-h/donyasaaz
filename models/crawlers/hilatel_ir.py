import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def hilatel(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.find("span", attrs={"itemprop": "price"})
    a = re.sub(r',', '', p.text).strip()
    b = re.split(r'\s', a)
    if b[0] == 'ناموجود':
        return -1
    else:
        return int(b[0])
