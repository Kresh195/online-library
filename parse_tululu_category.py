from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_books_urls(first_page, last_page):
    url = "https://tululu.org/l55/"
    books_selector = "table.d_book"
    book_page_url_list = list()
    for page in range(first_page, last_page + 1):
        url = urljoin(url, str(page))
        soup = get_soup(url)
        books = soup.select(books_selector)
        book_page_url_list += [urljoin(url, book.find('a')['href']) for book in books]
    return book_page_url_list

