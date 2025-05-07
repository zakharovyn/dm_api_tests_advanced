from logging import getLogger

from services.api_mailhog.mailhog import ApiMailhog
from services.dm_api_account.dm_api_account import DMApiAccountFacade

logger = getLogger(__name__)


class AccountMailhogFacade:
    def __init__(
            self,
            dm_api_account: DMApiAccountFacade,
            api_mailhog: ApiMailhog
    ):
        self.account = dm_api_account
        self.mailhog = api_mailhog

    def activate_user(
            self,
            login: str,
            status_code: int = 200
    ):
        logger.info(f'Активация пользователя {login}')
        token = self.mailhog.mailhog_api.get_token_by_login(login=login)
        response = self.account.account_api.activate_user(
            token=token,
            status_code=status_code
        )
        return response

    def change_password(
            self,
            login: str,
            old_password: str,
            new_password: str,
            status_code: int = 200,
            **kwargs
    ):
        logger.info(f'Изменение пароля для пользователя {login}')
        token = self.mailhog.mailhog_api.get_token_by_login(
            login=login,
            reset_password=True
        )
        response = self.account.account_api.change_password(
            login=login,
            old_password=old_password,
            new_password=new_password,
            token=token,
            status_code=status_code,
            **kwargs
        )
        return response

    def register_and_activate_user(
            self,
            login: str,
            email: str,
            password: str,
            **kwargs
    ):
        """Регистрация и активация пользователя"""
        logger.info(
            f'Регистрация нового пользователя с данными {login}, {password}, '
            f'{email}'
        )
        self.account.account_api.register_new_user(
            login=login,
            email=email,
            password=password
        )
        return self.activate_user(login=login)
