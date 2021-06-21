import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def maralkish(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    button = soup.find(attrs={"id": "btnAddToBasket"})
    if button is None or 'unavailable' in button.attrs['class']:
        return -1
    p = soup.find("span", attrs={"itemprop": "price"})
    a = re.sub(r',', '', p.text).strip()
    b = re.findall(r'\d+', a)
    return int(b[0])
