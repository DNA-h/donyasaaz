import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def m3sell(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("div", attrs={"class": "button__btn-normal-success___1JY6- button__btn-normal___299V7 button__btn___3Wejk button__success___2V0M8  styles__buy-button___11qld "}):
        div = soup.find("span", attrs={"class": "styles__final-price___1L1AM"})
        if div is None:
            return -2
        else:
            from persiantools import digits
            # digits.fa_to_en("0123456789")
            print(div.text)
            print(digits.fa_to_en(div.text))
            a = re.sub(r',', '', digits.fa_to_en(div.text)).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -3
