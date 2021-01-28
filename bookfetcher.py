import logging

import requests

logger = logging.getLogger('parser.main')


def check_for_redirect(response: requests.models.Response):
    """Проверяет наличие редиректа."""
    if response.history:
        raise requests.exceptions.HTTPError


def get_response(url: str) -> requests.models.Response:
    """получает ответ на запрос по url."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    }
    response = requests.get(url=url, headers=headers, verify=False)  # noqa: S501
    response.raise_for_status()
    check_for_redirect(response)
    return response
