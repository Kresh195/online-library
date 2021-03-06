import requests
import os
from pathlib import Path
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


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
    return name, author


def download_txt(response, filename, folder='books/'):
    txt_name = f'{sanitize_filename(filename)}.txt'
    filepath = os.path.join(folder, txt_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_book_image_url(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    image_link_part = soup.find('div', class_='bookimage').find('img')['src']
    image_link = urljoin('https://tululu.org', image_link_part)
    return image_link


def download_image(image_link, folder='images/'):
    response = requests.get(image_link)
    response.raise_for_status()
    image_name = image_link.split('/')[-1]
    filepath = os.path.join(folder, image_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_comments(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    comments = soup.find_all('div', class_='texts')
    comments_list = [comment_book.find('span', class_='black').text for comment_book in comments]
    return comments_list


def get_book_genres(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    genres = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres]
    return genres


def parse_book_page(book_url, book_id):
    url = book_url.format(book_id)
    name, author = get_book_info(url)
    genres = get_book_genres(url)
    comments = download_comments(url)
    image_link = get_book_image_url(url)
    book_page_info = {
        'name': name,
        'authoenr': author,
        'genres': genres,
        'comments': comments,
        'image_link': image_link
    }
    return book_page_info


def main():
    books_folder = 'books'
    images_folder = 'images'
    books_downloading_url = 'https://tululu.org/txt.php'
    book_url = 'https://tululu.org/b{}/'
    creating_folder(books_folder)
    creating_folder(images_folder)
    for book_id in range(1, 11):
        params = {
            'id': book_id
        }
        response = requests.get(books_downloading_url, params=params)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            book_name = get_book_info(book_url.format(book_id))
            # download_txt(response, book_name)
            image_link = get_book_image_url(book_url.format(book_id))
            # download_image(image_link)
            comments = download_comments(book_url.format(book_id))
            genres = get_book_genres(book_url.format(book_id))
            print(parse_book_page(book_url, book_id))
        except requests.exceptions.HTTPError:
            print(f'?????????? ?? id{book_id} ???? ????????????????????')


if __name__ == "__main__":
    main()
