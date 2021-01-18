import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

server = Server()

with open('books.json', 'r', encoding='utf8') as json_file:
    raw_books = json_file.read()
books = json.loads(raw_books)


def on_reload():
    """Render template."""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')
    rendered_page = template.render({'books': books})
    with open('index.html', 'w', encoding='utf8') as html_file:
        html_file.write(rendered_page)


server.watch('template.html', on_reload)
server.serve()
