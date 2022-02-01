import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def sedastore(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button" , attrs = {"class" : "btn btn-secondary btn-lg"}):
        # https://sedastore.com/product/%d9%87%d8%af%d9%81%d9%88%d9%86-hd-280-pro-%d8%b3%d9%86%d9%87%d8%a7%db%8c%d8%b2%d8%b1/
        p = soup.find("div", attrs={"id": "price"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[len(b)-1])
    else:
        return -1