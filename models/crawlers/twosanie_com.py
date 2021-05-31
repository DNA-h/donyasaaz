import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def twosanie(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("a", attrs={"class": "btn btn-block btn-lg btn-best-seller btn-danger m-auto"}):
        s = soup.find("div",attrs={"class":"product-price pt-lg-5 mb-xl-5 pb-xl-5"})
        if s is not None:
            a = re.sub(r',', '', s.text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
    else:
        return -1
