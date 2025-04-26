import random
from datetime import datetime
from types import SimpleNamespace

import pytest
import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

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
def mailhog():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    return MailHogApi(configuration=mailhog_configuration)


@pytest.fixture(scope='session')
def dm_api():
    dm_api_configuration = DmApiConfiguration(host=' http://5.63.153.31:5051')
    return DMApiAccount(configuration=dm_api_configuration)


@pytest.fixture(scope='session')
def account_helper(mailhog, dm_api):
    return AccountHelper(dm_account_api=dm_api, mailhog=mailhog)


@pytest.fixture(scope='session')
def auth_account_helper(mailhog):
    dm_api_configuration = DmApiConfiguration(host=' http://5.63.153.31:5051')
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    data = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    user = SimpleNamespace(
        login=f'test_user_advanced_{data}',
        password=f'test_password_advanced{data}',
        email=f'test_user_advanced_{data}@mail.ru'
    )
    account_helper.full_register_new_user(
        login=user.login,
        password=user.password,
        email=user.email
    )
    account_helper.auth_client(login=user.login, password=user.password)
    return SimpleNamespace(account_helper=account_helper, user=user)


@pytest.fixture
def prepare_user(account_helper):
    num = random.randint(a=0, b=1000)
    data = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    login: str = f'test_user_advanced_{data}{num}'
    password: str = f'test_password_advanced{data}{num}'
    email: str = f'{login}{num}@mail.ru'
    return SimpleNamespace(login=login, password=password, email=email)
