import random

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from utils import get_activation_token_by_login


def test_post_v1_account_login():
    # Регистрация пользователя
    postfix: str = str(random.randint(a=0, b=1000))
    account_api = AccountApi()
    mailhog_api = MailhogApi()

    login: str = f'test_user_advanced_{postfix}'
    password: str = f'test_password_advanced{postfix}'
    email: str = f'{login}@mail.ru'
    json_data: dict = {
        "login": login,
        "email": email,
        "password": password
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Письма не были получены'

    # Получить активационный токен
    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f'Токен для пользователя {login} не был получен'

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'Пользователь не был активирован'
