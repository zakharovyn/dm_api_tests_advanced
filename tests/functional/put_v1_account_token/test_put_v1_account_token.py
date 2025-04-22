import random

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from utils import get_activation_token_by_login


def test_put_v1_account_token():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host=' http://5.63.153.31:5051')

    mailhog_api = MailhogApi(configuration=mailhog_configuration)
    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)

    postfix: str = str(random.randint(a=0, b=1000))
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
