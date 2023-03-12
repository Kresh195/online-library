import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

os.makedirs("Pages", exist_ok=True)

def render_page():
    template = env.get_template('template.html')
    with open("media/books.json", "r", encoding="UTF8") as file:
        books = file.read()
    books = json.loads(books)
    pages_books = chunked(books, 10)
    for page, page_books in enumerate(pages_books, 1):
        chunked_books = chunked(page_books, 2)
        rendered_page = template.render(
            chunked_books=chunked_books
        )
        with open(f"Pages//index{page}.html", "w", encoding="UTF8") as file:
            file.write(rendered_page)


render_page()
# server = Server()
# server.watch('*.html', render_page)
# server.serve(root='.')
