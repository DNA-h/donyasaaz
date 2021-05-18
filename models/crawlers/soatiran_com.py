import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def soatiran(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if len(soup.find_all("button", attrs={"class": re.compile("single_add_to_cart_button*")})) > 0:
        div = soup.find("p", attrs={"class": "price"})
        if div is None:
            return -1
        p = div.find_all("ins")
        if len(p) > 0:
            a = re.sub(r',', '', p[0].text).strip()
        else:
            p = div.find_all("bdi")
            if len(p) == 0:
                return -1
            else:
                a = re.sub(r',', '', p[0].text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
