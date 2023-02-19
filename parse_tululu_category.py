from urllib.parse import urljoin

from get_soup import get_soup


def get_books_urls(first_page, last_page):
    url = "https://tululu.org/l55/"
    books_selector = "table.d_book"
    book_pages_urls = list()
    for page in range(first_page, last_page + 1):
        url = urljoin(url, str(page))
        soup = get_soup(url)
        books = soup.select(books_selector)
        book_pages_urls += [urljoin(url, book.find('a')['href']) for book in books]
    return book_pages_urls
