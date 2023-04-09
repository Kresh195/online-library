import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def render_page(env):
    template = env.get_template('template.html')
    with open("media/books.json", "r", encoding="UTF8") as file:
        books = file.read()
    books = json.loads(books)
    pages_books = list(chunked(books, 10))
    pages_count = len(pages_books)
    for page, page_books in enumerate(pages_books, 1):
        chunked_books = chunked(page_books, 2)
        rendered_page = template.render(
            pages_count=pages_count,
            chunked_books=chunked_books,
            current_page=page
        )
        with open(f"docs/index{page}.html", "w", encoding="UTF8") as file:
            file.write(rendered_page)


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    os.makedirs("docs", exist_ok=True)
    render_page(env)


if __name__ == "__main__":
    main()
# server = Server()
# server.watch('*.html', render_page)
# server.serve(root='.')
