import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def digiseda(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button", attrs={"class": "exclusive btn btn-success"}) or soup.find("div", attrs={"div": "call_to_buy no-print"}):
        p = soup.find("div", attrs={"id": "our_price_display"})
        s = re.sub(r'\s+', ' ', p.text).strip()
        a = re.sub(r',', '', s)
        b = re.findall(r'\d+', a)
        if int(b[0]) == 0:
            # return -1
            print("0")
        else:
            # return int(b[0])
            print("1")
    else:
        # return -1
        print("0")