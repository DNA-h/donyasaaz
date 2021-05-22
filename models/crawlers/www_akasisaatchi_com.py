import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def akasisaatchi(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    p = soup.find("p", attrs={"class": "price"})
    if p is not None:
        s = p.find("span")
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
    else:
        return -1