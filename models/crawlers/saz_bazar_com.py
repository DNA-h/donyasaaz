import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

def saz_bazar(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    div =  soup.find("div",attrs={"id":"product-availability"})
    if div is None or "ناموجود" in div.text:
        return -1

    p = soup.find("div", attrs={"class": "current-price"})
    if p is not None:
        s = p.find("span", attrs={"itemprop": "price"})
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        if a == 'تماس بگیرید':
            return -1
        else:
            return int(b[0])
    return -1


# class MyObject:
#     def __init__(self, url):
#         self.url = url
#
#
# item = MyObject("https://saz-bazar.com/baby-music/55-2633-%D8%A8%D9%84%D8%B2-2-%D8%A7%DA%A9%D8%AA%D8%A7%D9%88-%D8%B1%D9%87%D8%A7.html#/16-%D8%B1%D9%86%DA%AF-%D8%B2%D8%B1%D8%AF/25-%DA%AF%D8%A7%D8%B1%D8%A7%D9%86%D8%AA%DB%8C-%DA%AF%D8%A7%D8%B1%D8%A7%D9%86%D8%AA%DB%8C_%D8%A7%D8%B5%D8%A7%D9%84%D8%AA_%D9%88_%D8%B3%D9%84%D8%A7%D9%85%D8%AA_%D9%81%DB%8C%D8%B2%DB%8C%DA%A9%DB%8C")
# print(saz_bazar(item, None, None))
#
# item = MyObject("https://saz-bazar.com/pianos-keybord-organ/2330-2533-%D9%BE%DB%8C%D8%A7%D9%86%D9%88-%D8%AF%DB%8C%D8%AC%DB%8C%D8%AA%D8%A7%D9%84-%D9%85%D8%AF%D9%84-clp735.html")
# print(saz_bazar(item, None, None))