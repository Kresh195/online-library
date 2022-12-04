from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_book_url(url, soup):
    books = soup.find("td", class_="ow_px_td").find_all("table")
    for book in books:
        book_id = book.find("a")["href"]
        book_url = urljoin(url, book_id)
        print(book_url)


def main():
    url = "https://tululu.org/l55/"
    for page in range(1, 5):
        url = urljoin(url, f"{page}")
        soup = get_soup(url)
        get_book_url(url, soup)


if __name__ == "__main__":
    main()
