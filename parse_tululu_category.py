from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_books_urls():
    url = "https://tululu.org/l55/"
    books_selector = "table.d_book"
    for page in range(1, 2):
        url = urljoin(url, f"{page}")
        soup = get_soup(url)
        books = soup.select(books_selector)
        url_list = [urljoin(url, book.find('a')['href']) for book in books]
    return url_list

