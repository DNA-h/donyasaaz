import re
import logging
import math
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def headroom(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)

        return None

    div = soup.find("input", attrs={"class": "sabade-kharid"})
    if div is not None:
        p = soup.find(
            lambda tag: tag.name == "div" and "قيمت با تخفيف" in tag.text and
                        'class' in tag.attrs and 'feature' in tag.attrs['class'])
        if p is None:
            p = soup.find(
            lambda tag: tag.name == "div" and "قيمت کالا" in tag.text and
                        'class' in tag.attrs and 'feature' in tag.attrs['class'])
        if p is None:
            return -1
        a = re.sub(r',', '', p.text).strip()
        b = re.findall(r'\d+', a)
        return math.floor(int(b[0]) / 10)
    else:
        return -1
