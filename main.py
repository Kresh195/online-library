import requests
from pathlib import Path
from urllib.error import HTTPError


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


def main():
    folder = 'books'

    creating_folder(folder)
    downloading_books(folder)


if __name__ == "__main__":
    main()