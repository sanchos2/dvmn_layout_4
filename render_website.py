import json
import math
import os

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

load_dotenv()
server = Server()

with open('books.json', 'r', encoding='utf8') as json_file:
    raw_books = json_file.read()
books = json.loads(raw_books)

os.makedirs('pages', exist_ok=True)
pages = math.ceil(len(books) / int(os.getenv('BOOK_PER_PAGE', 10)))


def on_reload():
    """Render template."""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')
    for page, chunk in enumerate(chunked(books, int(os.getenv('BOOK_PER_PAGE', 10))), 1):
        rendered_page = template.render({'chunk': chunk, 'pages': pages, 'page': page})
        with open(f'index{page}.html', 'w', encoding='utf8') as html_file:
            html_file.write(rendered_page)


server.watch('template.html', on_reload)
server.serve(default_filename='index1.html')
