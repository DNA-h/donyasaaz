import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def technicav(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button", attrs={"class": "btn-full-disabled"}):
        return -1
    else:
        details = soup.find("div", attrs={"class": "product-details"})
        if details.find("div", attrs={"class": "product-price"}):
            if details.find("div",attrs={"class": "old-price"}):
                div = details.find("div",attrs={"class": "new-price"})
                a = re.sub(r',', '', div.text).strip()
                b = re.findall(r'\d+', a)
                return int(b[0])  
            else:
                return -1 
        else:
            return -1
              
        
        