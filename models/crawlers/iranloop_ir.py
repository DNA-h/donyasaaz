import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def iranloop(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("p", attrs={"id": "availability_statut"}).text == ' در انبار موجود نیست':
        return -1
    else:
        p = soup.find("p", attrs={"class": "our_price_display"})
        s = soup.find("span", attrs={"id": "our_price_display"})
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
