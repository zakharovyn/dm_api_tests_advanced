import random

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


def test_put_v1_account_email():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host=' http://5.63.153.31:5051')

    mailhog = MailHogApi(configuration=mailhog_configuration)
    account = DMApiAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    postfix: str = str(random.randint(a=0, b=1000))
    login: str = f'test_user_advanced_{postfix}'
    password: str = f'test_password_advanced{postfix}'
    email: str = f'{login}@mail.ru'

    account_helper.full_register_new_user(
        login=login, password=password, email=email
    )
    account_helper.user_login(login=login, password=password)

    # Изменить почту
    new_email = postfix + email
    account_helper.change_email(
        login=login, password=password, new_email=new_email
    )

    # Авторизоваться
    account_helper.user_login(login=login, password=password, status_code=403)

    # Получить письма из почтового сервера
    response = account_helper.get_messages()

    # Получить активационный токен
    token = account_helper.get_activation_token_by_login(
        login=login, response=response
    )

    # Активация пользователя
    account_helper.activate_user(token=token)

    # Авторизоваться
    account_helper.user_login(login=login, password=password)
