import re
import math
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def tasvirancam(link, headers, site):
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get(link.url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.info('%s :  %s,', site, e)
        
        return None

    div = soup.find("div", attrs={"id": "mc_lbPrice"})
    if div is None:
        return -1
    a = re.sub(r',', '', div.text).strip()
    b = re.findall(r'\d+', a)
    if len(b) == 0:
        return -1
    return  math.floor(int(b[0])/10)
