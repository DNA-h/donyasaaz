import re

import requests
from bs4 import BeautifulSoup


def esam(link, headers, site):
    try:
        response = requests.get(link.url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(site)
        print(e)
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
