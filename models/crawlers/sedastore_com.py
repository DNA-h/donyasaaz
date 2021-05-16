import re

import requests
from bs4 import BeautifulSoup


def sedastore(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button" , attrs = {"name" : "add-to-cart"}):
        # https://sedastore.com/product/%d9%87%d8%af%d9%81%d9%88%d9%86-hd-280-pro-%d8%b3%d9%86%d9%87%d8%a7%db%8c%d8%b2%d8%b1/
        p = soup.find("p", attrs={"class": "price"})
        if p.find("ins") != None:
            s = p.find("ins")
        else:
            s = p.find("bdi")
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1