import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def pianokadeh(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    s= soup.find("div", attrs={"class": "wz-shop-product-out-stock"})
    if s is None:
        q = soup.find("span",attrs={"id": "wz-product-price"})
        intab='۱۲۳۴۵۶۷۸۹۰١٢٣٤٥٦٧٨٩٠'
        outtab='12345678901234567890'
        translation_table = str.maketrans(intab, outtab)
        output_text = q.text.translate(translation_table)
        a = re.sub(r',', '', output_text).strip()
        b = re.findall(r'\d+', a)
        if len(b) == 0:
            return -1
        return int(b[0])
    else:
        return -1