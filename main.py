import os
import argparse
from urllib.parse import urljoin
from time import sleep
import json

import requests
from pathlib import Path
from pathvalidate import sanitize_filename

from parse_tululu_category import get_books_urls
from get_soup import get_soup
from check_for_redirect import check_for_redirect


def get_book_headers(soup):
    title, author = soup.select_one('h1').text.split('::')
    title = title.strip()
    author = author.strip()
    return title, author


def download_txt(response, book_name, folder='media/books/'):
    txt_name = f'{sanitize_filename(book_name)}.txt'
    book_path = os.path.join(folder, txt_name)
    with open(book_path, 'wb') as file:
        file.write(response.content)
    return book_path


def get_book_image_url(soup, url):
    image_link_part = soup.select_one('div.bookimage img')['src']
    image_link = urljoin(url, image_link_part)
    return image_link


def download_image(image_link, folder='media/images/'):
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
    book_description = {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': comments,
        'description': description
    }
    return book_description


def main():
    books_folder = 'books'
    images_folder = 'images'
    books_downloading_url = 'https://tululu.org/txt.php'
    parser = argparse.ArgumentParser(description='Программа скачивает книги из онлайн-библиотеки')
    parser.add_argument(
        '--first_page',
        '--start_page',
        default=1,
        type=int,
        help='Первая страница для загрузки книг'
    )
    parser.add_argument(
        '--last_page',
        '--end_page',
        default=4,
        type=int,
        help='Последняя страница для загрузки книг'
    )
    parser.add_argument(
        '--dest_folder',
        default='media',
        type=str,
        help='Путь к каталогу с результатами парсинга'
    )
    parser.add_argument(
        '--json_path',
        default='media',
        type=str,
        help='Путь к JSON файлу с результатами'
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Не скачивать картинки'
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Не скачивать тексты книг'
    )
    args = parser.parse_args()
    Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
    Path(f'{args.dest_folder}/{books_folder}').mkdir(parents=True, exist_ok=True)
    Path(f'{args.dest_folder}/{images_folder}').mkdir(parents=True, exist_ok=True)
    books_urls = get_books_urls(args.first_page, args.last_page)
    books_descriptions = list()
    for url in books_urls:
        book_id = int(url.split('b')[1].split('/')[0])
        params = {
            'id': book_id
        }
        soup = get_soup(url)
        try:
            response = requests.get(books_downloading_url, params=params)
            response.raise_for_status()
            check_for_redirect(response)
            book_description = parse_book_page(soup)
            book_title = book_description['title']
            if not args.skip_txt:
                book_path = download_txt(response, book_title, os.path.join(args.dest_folder, 'books'))
                book_description['book_path'] = book_path
            if not args.skip_imgs:
                image_link = get_book_image_url(soup, url)
                image_src = download_image(image_link, os.path.join(args.dest_folder, 'images'))
                book_description['image_src'] = image_src
            books_descriptions.append(book_description)
        except requests.exceptions.HTTPError:
            print(f'Книги с id{book_id} не существует')
        except requests.exceptions.ConnectionError:
            print('Повторное подключение')
            sleep(20)
    with open(os.path.join(args.json_path, 'books.json'), 'w', encoding='utf8') as books_json_file:
        json.dump(books_descriptions, books_json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
