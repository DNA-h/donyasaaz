import re

import requests
from bs4 import BeautifulSoup


def rayanseda(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger.info('%s :  %s,', site, e)
        
        return None

    if soup.find("button" , attrs = {"id" : "button-cart"}):
        p = soup.find("div", attrs={"class": "col-md-6 col-12 cost-product"})
        # https://rayanseda.com/%D9%85%DB%8C%D8%AF%DB%8C_%DA%A9%DB%8C%D8%A8%D9%88%D8%B1%D8%AF_Novation_49%20SL%20MKII
        if p.find("span", attrs={"class": "row-off-cost"}):
            s = p.find("span", attrs={"class": "row-off-cost"})
        else:
            s = p.find("span", attrs={"class": "prise-row orginal"})
        a = re.sub(r',', '', s.text).strip()
        b = re.findall(r'\d+', a)
        if int(b[0]) == 0:
            return -1

        else:
            return int(b[0])
    else:
        return -1
