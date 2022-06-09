import requests
from pathlib import Path
from urllib.error import HTTPError
from bs4 import BeautifulSoup



def creating_folder(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


def downloading_books(folder):
    books_downloading_url = "https://tululu.org/txt.php"
    for book_id in range(1, 11):
        params = {
            'id': book_id
        }
        response = requests.get(books_downloading_url, params=params)
        try:
            check_for_redirect(response)
            filename = f'{folder}/{book_id}.txt'
            with open(filename, 'wb') as file:
                file.write(response.content)
        except requests.exceptions.HTTPError:
            print(f'Книги {book_id} не существует')
            continue


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_book_info():
    url = 'https://tululu.org/b1/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('h1').text.split('::')[0].strip()
    author = soup.find('h1').text.split('::')[1].strip()
def main():
    folder = 'books'

    creating_folder(folder)
    # downloading_books(folder)
    get_book_info()


if __name__ == "__main__":
    main()