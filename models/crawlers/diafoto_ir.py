import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def diafoto(link, headers, site):
    return -1 # سایت دان هست