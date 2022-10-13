import os
import argparse
from urllib.parse import urljoin
from time import sleep

import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def get_book_title(soup):
    title = soup.find('h1').text.split('::')[0].strip()
    return title


def get_book_author(soup):
    author = soup.find('h1').text.split('::')[1].strip()
    return author


def get_book_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def download_txt(response, filename, folder='books/'):
    txt_name = f'{sanitize_filename(filename)}.txt'
    filepath = os.path.join(folder, txt_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_book_image_url(soup):
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


def download_comments(soup):
    comments = soup.find_all('div', class_='texts')
    comments = [comment_book.find('span', class_='black').text for comment_book in comments]
    return comments


def get_book_genres(soup):
    genres = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres]
    return genres


def parse_book_page(book_url, book_id):
    url = book_url.format(book_id)
    soup = get_book_soup(url)
    title = get_book_title(soup)
    author = get_book_author(soup)
    genres = get_book_genres(soup)
    comments = download_comments(soup)
    image_link = get_book_image_url(soup)
    all_about_book = {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': comments,
        'image_link': image_link
    }
    return all_about_book


def main():
    books_folder = 'books'
    images_folder = 'images'
    books_downloading_url = 'https://tululu.org/txt.php'
    book_url = 'https://tululu.org/b{}/'
    parser = argparse.ArgumentParser(description='Программа скачивает книги из онлайн-библиотеки')
    parser.add_argument('--start_id', default=1, type=int)
    parser.add_argument('--end_id', default=11, type=int)
    args = parser.parse_args()
    Path(books_folder).mkdir(parents=True, exist_ok=True)
    Path(images_folder).mkdir(parents=True, exist_ok=True)
    for book_id in range(args.start_id, args.end_id + 1):
        params = {
            'id': book_id
        }
        response = requests.get(books_downloading_url, params=params)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            book_title = parse_book_page(book_url, book_id)['title']
            download_txt(response, book_title)
            image_link = parse_book_page(book_url, book_id)['image_link']
            download_image(image_link)
        except requests.exceptions.HTTPError:
            print(f'Книги с id{book_id} не существует')
        except requests.exceptions.ConnectionError:
            print('Повторное подключение')
            sleep(20)


if __name__ == "__main__":
    main()
