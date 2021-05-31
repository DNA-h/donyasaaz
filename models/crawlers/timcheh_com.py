import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def timcheh(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    if soup.find("button", attrs={"class": "styles_custom_btn__2kID6 styles_btn_fill_48__2tZCA product_styles_add_to_cart_btn__3bn2P"}):
        div = soup.find("div",attrs={"class":"product_styles_info_price__3P4Ei"})
        if div is None:
            return -1
        p = div.find("span", attrs={"class":"product_styles_price__3Ws3t"})
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
