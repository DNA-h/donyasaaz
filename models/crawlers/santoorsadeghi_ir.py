import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def santoorsadeghi(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
        div = soup.find("p", attrs={"class": "price product-page-price"})
        if div is None:
            return -1
        p = div.find_all("span", attrs={"class": "woocommerce-Price-amount amount"})
        if len(p) == 0:
            return -1
        elif len(p) == 1:
            a = re.sub(r',', '', p[0].text).strip()
        else:
            a = re.sub(r',', '', p[1].text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1



# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://santoorsadeghi.ir/product/%d8%b3%d9%86%d8%aa%d9%88%d8%b1-%d8%b5%d8%a7%d8%af%d9%82%db%8c-%da%af%d9%84%d8%af%d8%a7%d8%b1-%db%8c%da%a9-%d9%85%d9%87%d8%b1/")
# print(santoorsadeghi(item, None, None))