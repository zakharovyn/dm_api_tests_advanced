from contextlib import contextmanager

import requests
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        exp_status_code: requests.codes = requests.codes.OK,
        exp_message: str = '',
        error: str = None
):
    try:
        yield
        if exp_status_code != requests.codes.OK:
            raise AssertionError(
                f'Ожидаемый статус код должен быть равен {exp_status_code}'
            )
        if exp_message:
            raise AssertionError(
                f'Должно быть получено сообщение: "{exp_message}", но запрос '
                f'прошел успешно'
            )
    except HTTPError as e:
        assert e.response.status_code == exp_status_code
        assert e.response.json()['title'] == exp_message
        if error:
            assert e.response.json()['errors'] == error
