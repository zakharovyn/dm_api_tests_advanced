import logging

from collections import namedtuple
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace


import pytest
import structlog
from vyper import v

from generic.utilites.rand_utils import generate_user_name, generate_password, generate_user_email
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

options = {
    'service.dm_api_account',
    'service.mailhog'
}


@pytest.fixture(scope='session', autouse=True)
def set_config(request):
    config = Path(__file__).parent.joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='stg', help='run stg'
    )

    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = Configuration(host=v.get('service.mailhog'))
    rest_client = RestClient(configuration=mailhog_configuration)
    logger.info(f'Инициализация ApiMailhog')
    return ApiMailhog(
        configuration=mailhog_configuration,
        client=rest_client
    )


@pytest.fixture(scope='session')
def dm_account():
    dm_api_config = Configuration(host=v.get('service.dm_api_account'))
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
    dm_api_config = Configuration(host=v.get('service.dm_api_account'))
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
    login: str = generate_user_name()
    password: str = generate_password()
    email: str = generate_user_email()
    logger.info(
        f'Тестовые данные для регистрации пользователя: {login}, {password}, '
        f'{email}'
    )
    return SimpleNamespace(login=login, password=password, email=email)
