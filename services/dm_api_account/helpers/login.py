from restclient.client import RestClient
from services.dm_api_account.apis.login_api import LoginApi
from services.dm_api_account.models import LoginCredentials


class Login(LoginApi):

    def __init__(self, facade, client: RestClient, headers: dict = None):
        from services.dm_api_account.dm_api_account import DMApiAccountFacade
        super().__init__(client)
        self.facade: DMApiAccountFacade = facade

    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            need_json: bool = True,
            status_code: int = 200,
            **kwargs
    ):
        """Залогинить пользователя"""
        response = self._post_v1_account_login(
            json=LoginCredentials(
                login=login,
                password=password,
                rememberMe=remember_me
            ),
            need_json=need_json,
            status_code=status_code,
            **kwargs
        )
        return response

    def logout_user(
            self,
            status_code: int = 204,
            **kwargs
    ):
        """Разлогинить пользователя."""
        response = self._delete_v1_account_login(
            status_code=status_code,
            **kwargs
        )
        return response

    def logout_user_from_all_devices(
            self,
            status_code: int = 204,
            **kwargs
    ):
        """Разлогинить пользователя на всех устройствах"""
        response = self._delete_v1_account_login_all(
            status_code=status_code,
            **kwargs
        )
        return response

# ------------------------- Вспомогательные методы -----------------------------

    def get_auth_token(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        response = self.login_user(
            login=login,
            password=password,
            remember_me=remember_me
        )
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }

        return token

    def auth_client(self, login: str, password: str):
        """Авторизовация клиента"""
        token = self.get_auth_token(login=login, password=password)
        self.facade.set_headers(token)
