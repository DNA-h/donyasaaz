import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def qeshmkharid(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    s= soup.find("span", attrs={"id": "our_price_display"})
    if s is not None:
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        price = int(b[0])
        if price <= 1000:
            return -1
        return price
    else:
        return -1
