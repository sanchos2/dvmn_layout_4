import hashlib
import logging
import os
from typing import List, Optional, Union
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from bookfetcher import get_response

logger = logging.getLogger('parser.books_handler')


def get_hash(content: Union[bytes]) -> str:  # noqa: WPS110
    """Получает хеш содержимого."""
    hash_md5 = hashlib.md5()  # noqa: S303
    hash_md5.update(content)
    return hash_md5.hexdigest()


def get_book_description(soup) -> List[str]:
    """Получает название книги и автора."""
    title = soup.select_one('.ow_px_td h1')
    return [text.strip() for text in title.text.split('::')]


def get_book_genres(soup) -> Optional[List[str]]:
    """Получает жанр книги."""
    raw_genres = soup.select('.ow_px_td span.d_book a')
    if not raw_genres:
        return None
    return [genre.text for genre in raw_genres]


def get_book_comments(soup) -> Optional[List[str]]:
    """Получает коментарии к книге."""
    comment_tags = soup.select('.texts span')
    if not comment_tags:
        return None
    return [comment.text for comment in comment_tags]


def create_dir(path: str, folder: str) -> str:
    """Создает директорию."""
    directory = os.path.join(path, folder)
    os.makedirs(directory, exist_ok=True)
    return directory


def download_img(url: str, path: str, folder='image') -> Optional[str]:
    """Скачивает обложку книги."""
    create_dir(path, folder)
    response = get_response(url)
    soup = BeautifulSoup(response.text, 'lxml')
    img = soup.select_one('.bookimage img')
    if not img:
        return None
    abs_img_url = urljoin('https://tululu.org/', img['src'])
    raw_img = get_response(abs_img_url)
    img_name = get_hash(raw_img.content)
    path_to_file = os.path.join(folder, f'{img_name}.jpg').replace('\\', '/')  # noqa: WPS221
    with open(path_to_file, 'wb') as image:
        image.write(raw_img.content)
    return path_to_file


def download_txt(url: str, path: str, folder='books') -> str:
    """Скачивает текст книги."""
    create_dir(path, folder)
    response = get_response(url)
    filename = get_hash(response.text.encode('utf-8'))
    path_to_file = os.path.join(folder, f'{filename}.txt').replace('\\', '/')  # noqa: WPS221
    if response.headers['Content-Type'] == 'text/plain; charset="utf-8"':
        with open(path_to_file, 'w', encoding='utf8') as book:
            book.write(response.text)
    return path_to_file
