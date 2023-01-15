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
    url_list = []
    for page in range(1, 2):
        url = urljoin(url, f"{page}")
        soup = get_soup(url)
        books = soup.find("td", class_="ow_px_td").find_all("table")
        for book in books:
            book_id = book.find("a")["href"]
            book_url = urljoin(url, book_id)
            url_list.append(book_url)
    return url_list
