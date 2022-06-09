import requests
import os
from pathlib import Path
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def creating_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_book_info(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('h1').text.split('::')[0].strip()
    author = soup.find('h1').text.split('::')[1].strip()
    return name


def download_txt(response, filename, folder='books/'):
    txt_name = f'{sanitize_filename(filename)}.txt'
    filepath = os.path.join(folder, txt_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def main():
    folder = 'books'
    books_downloading_url = 'https://tululu.org/txt.php'
    book_url = 'https://tululu.org/b{}/'
    creating_folder(folder)
    for book_id in range(1, 11):
        params = {
            'id': book_id
        }
        response = requests.get(books_downloading_url, params=params)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            book_name = get_book_info(book_url.format(book_id))
            download_txt(response, book_name)
        except requests.exceptions.HTTPError:
            print(f'Книги с id{book_id} не существует')


if __name__ == "__main__":
    main()
