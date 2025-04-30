from restclient.client import RestClient
from services.dm_api_account.apis.account_api import AccountApi
from services.dm_api_account.models import (
    ResetPassword,
    ChangeEmail,
    ChangePassword,
    Registration,
)


class Account(AccountApi):

    def __init__(self, facade, client: RestClient, headers: dict = None):
        from services.dm_api_account.dm_api_account import DMApiAccountFacade
        super().__init__(client)
        self.facade: DMApiAccountFacade = facade

    def register_new_user(
            self,
            login: str,
            email: str,
            password: str,
            status_code: int = 201
    ):
        response = self._post_v1_account(
            json=Registration(
                login=login,
                email=email,
                password=password
            ),
            status_code=status_code
        )
        return response

    def get_current_user_info(
            self,
            status_code: int = 200,
            **kwargs
    ):
        response = self._get_v1_account(
            status_code=status_code,
            **kwargs
        )
        return response

    def activate_user(
            self,
            login: str,
            status_code: int = 200
    ):
        token = self.facade.mailhog.get_token_by_login(login=login)
        response = self._put_v1_account_token(
            status_code=status_code,
            token=token
        )
        return response

    def reset_password(
            self,
            login: str,
            email: str,
            status_code: int = 200,
            **kwargs
    ):
        response = self._post_v1_account_password(
            json=ResetPassword(
                login=login,
                email=email
            ),
            status_code=status_code,
            **kwargs
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
        token = self.facade.mailhog.get_token_by_login(
            login=login,
            reset_password=True
        )
        response = self._put_v1_account_password(
            json=ChangePassword(
                login=login,
                token=token,
                oldPassword=old_password,
                newPassword=new_password
            ),
            status_code=status_code,
            **kwargs
        )
        return response

    def change_email(
            self,
            login: str,
            password: str,
            new_email: str,
            status_code: int = 200,
            **kwargs
    ):
        response = self._put_v1_account_email(
            json=ChangeEmail(
                login=login,
                password=password,
                email=new_email
            ),
            status_code=status_code,
            **kwargs
        )
        return response

# ------------------------- Вспомогательные методы -----------------------------

    def register_and_activate_user(
            self,
            login: str,
            email: str,
            password: str,
            **kwargs
    ):
        """Регистрация и активация пользователя"""
        self.register_new_user(login=login, email=email, password=password)
        return self.activate_user(login=login)
