import json
import math
import os
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

load_dotenv()
server = Server()
book_per_page = int(os.getenv('BOOK_PER_PAGE', 10))

with open('books.json', 'r', encoding='utf8') as json_file:
    raw_books = json_file.read()
books = json.loads(raw_books)

os.makedirs('pages', exist_ok=True)
pages = math.ceil(len(books) / book_per_page)  # noqa: WPS221


def remove_files(template_path: str) -> None:
    """Удаляет файлы по шаблону."""
    for file in Path.cwd().glob(template_path):  # noqa: WPS110
        os.remove(file)


def on_reload() -> None:
    """Рендерид html страницы."""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')
    for page, chunk in enumerate(chunked(books, book_per_page), 1):  # noqa: WPS221
        rendered_page = template.render({'chunk': chunk, 'pages': pages, 'page': page})
        with open(os.path.join('pages', f'index{page}.html'), 'w', encoding='utf8') as html_file:  # noqa: WPS221
            html_file.write(rendered_page)


remove_files('pages/index?*.html')
on_reload()
server.watch('template.html', on_reload)
server.serve(root='pages')
