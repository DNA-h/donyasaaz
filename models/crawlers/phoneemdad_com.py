import re
import logging

import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def phoneemdad(link, headers, site):
    return -1 # قیمت نداره