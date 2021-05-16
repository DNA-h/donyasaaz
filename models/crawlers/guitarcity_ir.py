import re

import requests
from bs4 import BeautifulSoup


def guitarcity(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button", attrs={"class": "single_add_to_cart_button button alt"}):
        div = soup.find("div", attrs={"class": "summary entry-summary"})
        p =div.find("p",attrs={"class":"price"})
        a = re.sub(r',', '', p.text.replace(".","")).strip()
        b = re.findall(r'\d+', a)
        return int(b[0])
    else:
        return -1
