import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from urllib.parse import quote
from more_itertools import chunked
from dotenv import load_dotenv


JSON_PATH = os.getenv("JSON_PATH", default="media/books.json")


def on_reload():
    with open(JSON_PATH, "r", encoding="UTF8") as file:
        books_descriptions = json.load(file)
    books_on_page = 10
    pages_books = list(chunked(books_descriptions, books_on_page))
    pages_count = len(pages_books)
    columns_number = 2
    for page, page_books in enumerate(pages_books, 1):
        for book in page_books:
            book["image_src"] = quote(book["image_src"], safe="/")
            book["book_path"] = quote(book["book_path"], safe="/")
        chunked_books = chunked(page_books, columns_number)
        render_page(pages_count, chunked_books, page)


def render_page(pages_count, chunked_books, page):
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("./template.html")
    rendered_page = template.render(
        pages_count=pages_count,
        chunked_books=chunked_books,
        current_page=page
    )
    with open(f"pages/index{page}.html", "w", encoding="UTF8") as file:
        file.write(rendered_page)


def main():
    load_dotenv()

    os.makedirs("pages", exist_ok=True)
    on_reload()

    server = Server()
    server.watch("*.html", on_reload)
    server.serve(root=".")


if __name__ == "__main__":
    main()
