import os
import argparse
from urllib.parse import urljoin
from time import sleep
import json

import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from parse_tululu_category import get_books_urls

def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_book_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_headers(soup):
    title, author = soup.select_one('h1').text.split('::')
    title = title.strip()
    author = author.strip()
    return title, author


def download_txt(response, book_name, folder='books/'):
    txt_name = f'{sanitize_filename(book_name)}.txt'
    book_path = os.path.join(folder, txt_name)
    with open(book_path, 'wb') as file:
        file.write(response.content)
    return book_path


def get_book_image_url(soup, url):
    image_link_part = soup.select_one('div.bookimage img')['src']
    image_link = urljoin(url, image_link_part)
    return image_link


def download_image(soup, url, folder='images/'):
    image_link = get_book_image_url(soup, url)
    response = requests.get(image_link)
    response.raise_for_status()
    image_name = image_link.split('/')[-1]
    image_path = os.path.join(folder, image_name)
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return image_path


def download_comments(soup):
    comments = soup.select('div.texts')
    comments = [comment_book.select_one('span.black').text for comment_book in comments]
    return comments


def get_book_genres(soup):
    genres = soup.select('span.d_book a')
    genres = [genre.text for genre in genres]
    return genres


def get_book_descriptions(soup):
    description = soup.select('table.d_book')[1]
    description = description.text
    return description


def parse_book_page(soup):
    title, author = get_book_headers(soup)
    genres = get_book_genres(soup)
    comments = download_comments(soup)
    description = get_book_descriptions(soup)
    book = {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': comments,
        'description': description
    }
    return book


def main():
    books_folder = 'books'
    images_folder = 'images'
    books_downloading_url = 'https://tululu.org/txt.php'
    parser = argparse.ArgumentParser(description='Программа скачивает книги из онлайн-библиотеки')
    parser.add_argument('--first_page', default=1, type=int)
    parser.add_argument('--last_page', default=3, type=int)
    args = parser.parse_args()
    Path(books_folder).mkdir(parents=True, exist_ok=True)
    Path(images_folder).mkdir(parents=True, exist_ok=True)
    url_list = get_books_urls(args.first_page, args.last_page)
    books = list()
    for url in url_list:
        book_id = int(url.split('b')[1].split('/')[0])
        params = {
            'id': book_id
        }
        response = requests.get(books_downloading_url, params=params)
        soup = get_book_soup(url)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(soup)
            book_title = book['title']
            book_path = download_txt(response, book_title)
            image_src = download_image(soup, url)
            book['book_path'] = book_path
            book['image_src'] = image_src
            books.append(book)
        except requests.exceptions.HTTPError:
            print(f'Книги с id{book_id} не существует')
        except requests.exceptions.ConnectionError:
            print('Повторное подключение')
            sleep(20)
    books_json = json.dumps(books, ensure_ascii=False)
    with open('books.json', 'w', encoding='utf8') as books_json_file:
        books_json_file.write(books_json)


if __name__ == "__main__":
    main()
