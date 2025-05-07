import random
from collections import namedtuple
from datetime import datetime
from types import SimpleNamespace

import pytest
import structlog

from restclient.client import RestClient
from restclient.configuration import Configuration
from services.api_mailhog.apis.mailhog_api import MailhogApi
from services.api_mailhog.mailhog import ApiMailhog
from services.dm_api_account.dm_api_account import DMApiAccountFacade
from services.services_facade import AccountMailhogFacade

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
    return ApiMailhog(
        configuration=mailhog_configuration,
        client=rest_client
    )


@pytest.fixture(scope='session')
def dm_account():
    dm_api_config = Configuration(host=' http://5.63.153.31:5051')
    rest_client = RestClient(configuration=dm_api_config)
    return DMApiAccountFacade(
        configuration=dm_api_config,
        client=rest_client
    )


@pytest.fixture(scope='session')
def account_mh(dm_account, mailhog_api):
    return AccountMailhogFacade(
        dm_api_account=dm_account,
        api_mailhog=mailhog_api
    )


@pytest.fixture(scope='session')
def auth_account(mailhog_api):
    dm_api_config = Configuration(host=' http://5.63.153.31:5051')
    rest_client = RestClient(configuration=dm_api_config)
    account_facade = DMApiAccountFacade(
        configuration=dm_api_config,
        client=rest_client
    )
    account_mailhog = AccountMailhogFacade(
        dm_api_account=account_facade,
        api_mailhog=mailhog_api
    )
    data = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    user = SimpleNamespace(
        login=f'test_user_advanced_{data}',
        password=f'test_password_advanced{data}',
        email=f'test_user_advanced_{data}@mail.ru'
    )
    account_mailhog.register_and_activate_user(
        login=user.login,
        password=user.password,
        email=user.email
    )
    account_mailhog.account.auth_client(login=user.login, password=user.password)
    Config = namedtuple('Config', ['service', 'user'])
    return Config(service=account_mailhog, user=user)


@pytest.fixture
def prepare_user():
    num = random.randint(a=0, b=1000)
    data = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    login: str = f'test_user_advanced_{data}{num}'
    password: str = f'test_password_advanced{data}{num}'
    email: str = f'{login}{num}@mail.ru'
    return SimpleNamespace(login=login, password=password, email=email)
