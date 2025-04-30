import random
from datetime import datetime
from types import SimpleNamespace

import pytest
import structlog

from restclient.client import RestClient
from restclient.configuration import Configuration
from services.api_mailhog.apis.mailhog_api import MailhogApi
from services.dm_api_account.dm_api_account import DMApiAccountFacade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = Configuration(host='http://5.63.153.31:5025')
    rest_client = RestClient(configuration=mailhog_configuration)
    return MailhogApi(client=rest_client)


@pytest.fixture(scope='session')
def dm_account(mailhog_api):
    dm_api_config = Configuration(host=' http://5.63.153.31:5051')
    rest_client = RestClient(configuration=dm_api_config)
    return DMApiAccountFacade(
        configuration=dm_api_config,
        client=rest_client,
        mailhog=mailhog_api
    )


@pytest.fixture(scope='session')
def auth_account(mailhog_api):
    dm_api_config = Configuration(host=' http://5.63.153.31:5051')
    rest_client = RestClient(configuration=dm_api_config)
    account_facade = DMApiAccountFacade(
        configuration=dm_api_config,
        client=rest_client,
        mailhog=mailhog_api
    )
    data = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    user = SimpleNamespace(
        login=f'test_user_advanced_{data}',
        password=f'test_password_advanced{data}',
        email=f'test_user_advanced_{data}@mail.ru'
    )
    account_facade.account.register_and_activate_user(
        login=user.login,
        password=user.password,
        email=user.email
    )
    account_facade.login.auth_client(login=user.login, password=user.password)
    return SimpleNamespace(account=account_facade, user=user)


@pytest.fixture
def prepare_user():
    num = random.randint(a=0, b=1000)
    data = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    login: str = f'test_user_advanced_{data}{num}'
    password: str = f'test_password_advanced{data}{num}'
    email: str = f'{login}{num}@mail.ru'
    return SimpleNamespace(login=login, password=password, email=email)
