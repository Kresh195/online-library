import requests
from bs4 import BeautifulSoup

from check_for_redirect import check_for_redirect

def get_soup(url):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    return soup