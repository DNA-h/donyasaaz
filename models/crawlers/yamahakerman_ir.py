import re

import requests
from bs4 import BeautifulSoup


def yamahakerman(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    s= soup.findAll("span", attrs={"class": "woocommerce-Price-amount amount"})
    button = soup.find("button", attrs={"class":"single_add_to_cart_button button alt"})
    if button is None or s is None or len(s) <= 1:
        return -1
    else:
        if len(s) == 2:
            a = re.sub(r',', '', s[1].text).strip()
            b = re.findall(r'\d+', a)
            return int(b[0])
        else:
            if s[2].sourceline - s[1].sourceline <=10:
                a = re.sub(r',', '', s[2].text).strip()
                b = re.findall(r'\d+', a)
                return int(b[0])
            else:
                a = re.sub(r',', '', s[1].text).strip()
                b = re.findall(r'\d+', a)
                return int(b[0])
