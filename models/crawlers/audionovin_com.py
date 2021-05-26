import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def audionovin(link, headers, site):
    return -1 # سایت اصلا هیچ قیمتی ندارخ
    # try:
    #     requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    #     response = requests.get(link.url, headers=headers, verify=False)
    #     soup = BeautifulSoup(response.text, "html.parser")
    # except Exception as e:
    #     logger = logging.getLogger(__name__)
    #     logger.info('%s :  %s,', site, e)
    #     
    #     return None
    #
    # if soup.find("button", attrs={"name": "add-to-cart"}):
    #     p = soup.find("p", attrs={"class": "price"})
    #     if p.find("ins") is not None:
    #         s = p.find("ins")
    #     else:
    #         s = p.find("bdi")
    #     a = re.sub(r',', '', s.text).strip()
    #     b = re.findall(r'\d+', a)
    #     return int(b[0])
    # else:
    #     return -1
