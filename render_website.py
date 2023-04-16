import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def on_reload(pages_books):
    pages_count = len(pages_books)
    columns_number = 2
    for page, page_books in enumerate(pages_books, 1):
        chunked_books = chunked(page_books, columns_number)
        render_page(pages_count, chunked_books, page)


def render_page(pages_count, chunked_books, page):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        pages_count=pages_count,
        chunked_books=chunked_books,
        current_page=page
    )
    with open(f"docs/index{page}.html", "w", encoding="UTF8") as file:
        file.write(rendered_page)


def main():
    os.makedirs("docs", exist_ok=True)
    with open("media/books.json", "r", encoding="UTF8") as file:
        books = file.read()
    books = json.loads(books)
    books_on_page = 10
    pages_books = list(chunked(books, books_on_page))
    on_reload(pages_books)

    server = Server()
    server.watch('./template.html', on_reload(pages_books))
    server.serve(root='.')


if __name__ == "__main__":
    main()
