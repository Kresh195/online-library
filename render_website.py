import json
import os
import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def on_reload(pages_books, pages_count, columns_number):
    for page, page_books in enumerate(pages_books, 1):
        chunked_books = chunked(page_books, columns_number)
        render_page(pages_count, chunked_books, page)


def render_page(pages_count, chunked_books, page):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('./template.html')
    rendered_page = template.render(
        pages_count=pages_count,
        chunked_books=chunked_books,
        current_page=page
    )
    with open(f"pages/index{page}.html", "w", encoding="UTF8") as file:
        file.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(description='Программа запускает локальный сайт')
    parser.add_argument(
        '--json_path',
        default='media',
        type=str,
        help='Путь к JSON файлу с результатами'
    )
    args = parser.parse_args()

    os.makedirs("pages", exist_ok=True)
    with open(os.path.join(args.json_path, 'books.json'), "r", encoding="UTF8") as file:
        books_descriptions = json.load(file)
    books_on_page = 10
    pages_books = list(chunked(books_descriptions, books_on_page))
    pages_count = len(pages_books)
    columns_number = 2
    for page, page_books in enumerate(pages_books, 1):
        chunked_books = chunked(page_books, columns_number)
        render_page(pages_count, chunked_books, page)

    server = Server()
    server.watch('./template.html', on_reload(pages_books, pages_count, columns_number))
    server.serve(root='.')


if __name__ == "__main__":
    main()
