import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

with open('books.json', 'r', encoding='utf8') as json_file:
    raw_books = json_file.read()
books = json.loads(raw_books)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']),
)

template = env.get_template('template.html')
rendered_page = template.render({'books': books})

with open('index.html', 'w', encoding='utf8') as html_file:
    html_file.write(rendered_page)

server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
