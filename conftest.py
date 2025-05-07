import logging

import random
from collections import namedtuple
from datetime import datetime
from types import SimpleNamespace


import pytest
import structlog

from generic.utilites.rand_utils import get_random_string
from restclient.client import RestClient
from restclient.configuration import Configuration
from services.api_mailhog.mailhog import ApiMailhog
from services.dm_api_account.dm_api_account import DMApiAccountFacade
from services.services_facade import AccountMailhogFacade

logger = logging.getLogger(__name__)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


def pytest_addoption(parser):
    parser.addoption(
        '--log_level',
        default='warn',
        help='Selecting the logging level in the test',
        choices=('debug', 'info', 'warn', 'crit', 'err')
    )


@pytest.fixture(autouse=True)
def log(caplog, pytestconfig):
    level = pytestconfig.getoption('--log_level')
    caplog.get_records(when='call')
    match level:
        case 'debug':
            caplog.set_level(logging.DEBUG)
        case 'info':
            caplog.set_level(logging.INFO)
        case 'warn':
            caplog.set_level(logging.WARNING)
        case 'err':
            caplog.set_level(logging.ERROR)
        case 'crit':
            caplog.set_level(logging.CRITICAL)


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = Configuration(host='http://5.63.153.31:5025')
    rest_client = RestClient(configuration=mailhog_configuration)
    logger.info(f'Инициализация ApiMailhog')
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
    logger.info(f'Инициализация AccountMailhogFacade')
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
    logger.info(f'Инициализация авторизованного AccountMailhogFacade')
    return Config(service=account_mailhog, user=user)


@pytest.fixture
def prepare_user():
    random_string = get_random_string(length=12)
    login: str = f'test_user_{random_string}'
    password: str = f'test_password_{random_string}'
    email: str = f'{login}{random_string}@mail.ru'
    logger.info(
        f'Тестовые данные для регистрации пользователя: {login}, {password}, '
        f'{email}'
    )
    return SimpleNamespace(login=login, password=password, email=email)
