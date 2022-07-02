import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def papiran(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("div", attrs={"class": "styles__button-wrapper___tIUZJ"}):
        div = soup.find("span", attrs={"class": "styles__final-price___1L1AM"})
        if div is None:
            return -1
        elif len(div) == 1:
            a = re.sub(r',', '', div[0].text).strip()
        else:
            a = re.sub(r',', '', div[1].text).strip()
        b = re.findall(r'\d+', a)
        return div
    else:
        return -1
