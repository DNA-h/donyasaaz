import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def sazplus(link, headers, site):
    return -1
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
    # if soup.find("button", attrs={"class": "btn shenavarmobilebtn btn-md btn-success"}):
    #     p = soup.find("span", attrs={"class": "main-price main-pr-new mt-2"})
    #     if p is None:
    #         return -1
    #     else:
    #         a = re.sub(r'٬', '', p.text).strip()
    #     b = re.findall(r'\d+', a)
    #     return int(b[0])
    # else:
    #     return -1
