import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def aria_mall(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("span", attrs={"class": "btn btn-success"}):
        div = soup.find("span", attrs={"class": "tag"})
        if div is not None:
            s = div.find_all("h4")
            if len(s) == 0:
                return - 1
            if len(s) == 1:
                a = re.sub(r',', '', s[0].text).strip()
            else:
                a = re.sub(r',', '', s[len(s) - 1].text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        return -1
    else:
        return -1
