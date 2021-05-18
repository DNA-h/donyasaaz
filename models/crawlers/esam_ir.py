import re

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def esam(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("input" , attrs = {"class" : "btn btn-primary btn-buy SpaceMargin addToBasket"}):
        if soup.find("span" , attrs = {"class" : "text-danger DiscountLarge"}):
            p = soup.find("span" , attrs = {"class" : "text-danger DiscountLarge"})
            a = re.sub(r',', '', p.text).strip()
            b = re.findall(r'\d+', a)
        elif soup.find("span" , attrs = {"class" : "FixPrice DiscountLarge"}):
            p = soup.find("span" , attrs = {"class" : "FixPrice DiscountLarge"})
            a = re.sub(r',', '', p.text).strip()
            b = re.findall(r'\d+', a)
        if int(b[0]) == 0:
            return -1
        else:
            return int(b[0])
    else:
        return -1
