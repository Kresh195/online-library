import requests
import os
from pathlib import Path
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import argparse


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
    parser = argparse.ArgumentParser(description='Программа скачивает книги из онлайн-библиотеки')
    parser.add_argument('--start_id', default=1, type=int)
    parser.add_argument('--end_id', default=11, type=int)
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    creating_folder(books_folder)
    creating_folder(images_folder)
    for book_id in range(start_id, end_id):
        params = {
            'id': book_id
        }
        response = requests.get(books_downloading_url, params=params)
        try:
            response.raise_for_status()
            check_for_redirect(response)
            page_info = parse_book_page(book_url, book_id)
            book_name = page_info['name']
            download_txt(response, book_name)
            image_link = page_info['image_link']
            download_image(image_link)
        except requests.exceptions.HTTPError:
            print(f'Книги с id{book_id} не существует')


if __name__ == "__main__":
    main()
