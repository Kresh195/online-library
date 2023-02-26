import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def render_page():
    template = env.get_template('template.html')
    with open("media/books.json", "r", encoding="UTF8") as file:
        books = file.read()
    books = json.loads(books)
    rendered_page = template.render(
        books=books
    )
    with open("index.html", "w", encoding="UTF8") as file:
        file.write(rendered_page)


server = Server()
server.watch('*.html', render_page)
server.serve(root='.')
